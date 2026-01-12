import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import ChatMessageCreateForm
from .models import ChatGroup, GroupMessage
from .service.chat_service import ChatService
from .utility import private_room_name


@login_required(login_url="account_login")
def chat_base_view(request):
    chat_types = ["global", "group", "private"]

    return render(
        request,
        "chats/chat.html",
        {
            "chat_types": chat_types,
        }
    )


@login_required(login_url="account_login")
def chat_view(request, chat_type=None, chat_name=None):
    chat_types = ["global", "group", "private"]

    groups = None
    private_chats = None
    chat_group = None
    chat_messages = None
    active_group = None
    other_user = None
    members = []

    if chat_type == "global":
        groups = ChatGroup.objects.filter(chat_type="global")

    elif chat_type == "group":
        groups = ChatGroup.objects.filter(
            chat_type="group",
            members=request.user
        )

    elif chat_type == "private":
        private_chats = (
            ChatGroup.objects
            .filter(chat_type="private", members=request.user)
            .prefetch_related("members")
        )

        private_chats = [
            {
                "group": group,
                "other_user": group.members.exclude(id=request.user.id).first()
            }
            for group in private_chats
        ]

    elif chat_type is not None:
        raise PermissionDenied("Invalid chat type")

    if chat_type and chat_name:
        chat_group = ChatService.get_chat(chat_type, chat_name)

        if not chat_group:
            messages.warning(request, "Group does not exists.")
            return redirect("chat_type", chat_type=chat_type)

        if not chat_group.can_view(request.user):
            raise PermissionDenied("Invalid access")

        members = list(
            chat_group.members.values_list("username", flat=True)
        )

        chat_messages = (
            chat_group.chat_messages
            .select_related("author")
            .order_by("created_at")[:60]
        )

        if chat_group.chat_type == "private":
            other_user = chat_group.members.exclude(id=request.user.id).first()
            active_group = chat_group.display_name_for(request.user)
        else:
            active_group = chat_group.display_name

    return render(
        request,
        "chats/chat.html",
        {
            "chat_types": chat_types,
            "active_type": chat_type,

            "groups": groups,
            "private_chats": private_chats,

            "chat_group": chat_group,
            "chat_messages": chat_messages,
            "members": members,

            "active_group": active_group,
            "current_chat": chat_name,
            "other_user": other_user,

            "form": ChatMessageCreateForm(),
        }
    )


@login_required(login_url="account_login")
def create_group(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request"})

    name = f"{request.user.username}-group-{request.POST.get("group_name")}"
    desc = request.POST.get("description", "")
    members = json.loads(request.POST.get("members", "[]"))

    if ChatGroup.objects.filter(group_name=name).exists():
        return JsonResponse({"success": False, "error": "Group already exists"})

    group = ChatGroup.objects.create(
        group_name=name,
        description=desc,
        chat_type="group",
        creator=request.user
    )

    if request.POST.get("image_url"):
        group.image = request.POST.get("image_url")
        group.save()

    group.members.add(request.user)

    for username in members:
        try:
            user = User.objects.get(username=username)
            group.members.add(user)
        except User.DoesNotExist:
            pass

    return JsonResponse({"success": True})


@login_required(login_url="account_login")
@require_POST
def edit_group(request, chat_type=None, group_name=None):
    if not chat_type:
        return JsonResponse({"success": False, "error": "Invalid request"})

    group = get_object_or_404(ChatGroup, chat_type=chat_type, group_name=group_name)

    if request.user != group.creator:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if chat_type != "global":
        group_name = f"{request.user.username}-group-{request.POST.get("groupName")}"
    else:
        group_name = request.POST.get("groupName")

    group.group_name = group_name
    group.description = request.POST.get("description")

    if request.POST.get("image_url"):
        group.image_url = request.POST.get("image_url")

    if group.chat_type == "group":
        members = json.loads(request.POST.get("members", "[]"))

        users = list(
            User.objects.filter(username__in=members)
        )
        users.append(group.creator)

        group.members.set(users)

    group.save()

    return JsonResponse({"success": True, "group_name":group.group_name})


@login_required(login_url="account_login")
def start_private_chat(request, username):

    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.info(request, "User not found")
        return redirect("chat_type", chat_type="private")

    if other_user == request.user:
        messages.error(request, "You cannot start a chat with yourself")
        return redirect("chat_type", chat_type="private")

    group_name = private_room_name(request.user, other_user)

    with transaction.atomic():
        chat, created = ChatGroup.objects.get_or_create(
            group_name=group_name,
            chat_type="private",
            defaults={
                "description": "Private Chat",
                "creator": request.user,
            }
        )

        chat.members.add(request.user, other_user)

    return redirect("chat", chat_type="private", chat_name=group_name)


@login_required(login_url="account_login")
def upload_file(request, chat_type=None, chat_name=None):
    if not request.htmx:
        messages.warning(request, "Invalid request")
        return HttpResponseBadRequest("Invalid request")

    chat = get_object_or_404(
        ChatGroup,
        chat_type=chat_type,
        group_name=chat_name
    )

    file_message = ""
    file_url = request.POST.get("file_url")
    file_type = request.POST.get("file_type")
    file_name = request.POST.get("file_name")
    if request.POST.get("file_message"):
        file_message = request.POST.get("file_message")

    if chat_type != "global"  and request.user not in chat.members.all():
        messages.warning(request, "Unauthorized")
        return HttpResponseForbidden("You are not allowed")

    if not file_url or not file_name:
        messages.error(request, "Missing file data")
        return HttpResponseBadRequest("Missing file data")

    message = GroupMessage.objects.create(
        group=chat,
        author=request.user,
        message=file_message,
        file_url=file_url,
        file_type=file_type,
        file_name=file_name,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{chat_type}-{chat_name}",
        {
            "type": "message_handler",
            "message_id": message.id,
        }
    )

    return HttpResponse(status=204)


@login_required(login_url="account_login")
def leave_group(request, chat_type=None, chat_name=None):
    if not chat_type or not chat_name:
        messages.warning(request, "Invalid request")
        return redirect("chat_base")

    try:
        chat = ChatService.get_chat_404(chat_type, chat_name)
    except Http404:
        messages.error(request, "Group does not exist")
        return redirect("chat", chat_type=chat_type, chat_name=chat_name)

    if not ChatService.is_member(chat, request.user.id):
        messages.warning(request, "Unauthorized access")
        return redirect("chat_type", chat_type=chat_type)

    chat.members.remove(request.user)

    messages.success(request, "You have left the chat")
    return redirect("chat_type", chat_type=chat_type)


@login_required(login_url="account_login")
def delete_group(request, chat_type=None, chat_name=None):
    if not chat_type or not chat_name:
        messages.warning(request, "Invalid request")
        return redirect("chat_base")

    try:
        chat = ChatService.get_chat_404(chat_type, chat_name)
    except Http404:
        messages.error(request, "Group does not exist")
        return redirect("chat", chat_type=chat_type)

    if not chat.is_owner(request.user):
        messages.warning(request, "Unauthorized access")
        return redirect("chat_type", chat_type=chat_type)

    count = ChatService.delete_group(chat_type, chat_name)

    if count == 0:
        messages.error(request, "Unable to delete group")
        return redirect("chat_type", chat_type=chat_type, chat_name=chat_name)

    messages.success(request, "Group deleted Successfully")
    return redirect("chat_type", chat_type=chat_type)
