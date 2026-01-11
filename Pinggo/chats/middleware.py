from allauth.account.models import EmailAddress
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


EMAIL_VERIFIED_ROUTES = (
    "/chat/",
)

class EmailVerifiedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith(EMAIL_VERIFIED_ROUTES) and
            request.user.is_authenticated
        ):
            is_verified = EmailAddress.objects.filter(
                user=request.user,
                verified=True,
            ).exists()

            if not is_verified:
                messages.warning(request, "Please verify your email first.")
                return redirect(reverse("profile_settings"))

        return self.get_response(request)
