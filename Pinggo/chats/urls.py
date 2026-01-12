from django.urls import path

from .views import chat_base_view, chat_view, create_group, edit_group, start_private_chat, upload_file, leave_group, delete_group

urlpatterns = [
    path('', chat_base_view, name='chat_base'),
    path('create/', create_group, name='create_group' ),
    path('create/<str:username>/', start_private_chat, name='create_private_chat'),
    path('<str:chat_type>/', chat_view, name='chat_type'),
    path('<str:chat_type>/<str:chat_name>/', chat_view, name='chat'),
    path('edit/<str:chat_type>/<str:group_name>/', edit_group, name='update_group'),
    path('file-upload/<str:chat_type>/<str:chat_name>', upload_file, name="upload-file"),
    path('leave/<str:chat_type>/<str:chat_name>/', leave_group, name='leave_group'),
    path('delete/<str:chat_type>/<str:chat_name>/', delete_group, name='delete_group'),
]
