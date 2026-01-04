from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ..exception import ProfileDoesNotExist
from ..models import Profile



class UserService:

    @staticmethod
    def get_user_details_by_username(username) -> Profile:
        return get_object_or_404(User, username=username).profile

    @staticmethod
    def get_user_details_by_email(email) -> Profile:
        return get_object_or_404(User, email=email).profile

    @staticmethod
    def does_user_already_exist_by_username(user_id, username) -> bool:
        return User.objects.filter(username=username).exclude(pk=user_id).exists()

    @staticmethod
    def get_user_details(user):
        try:
            return user.profile
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist("User does not exist")

    @staticmethod
    def delete_user(request):
        request.user.delete()
        logout(request)

