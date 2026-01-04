from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.db import transaction



class EmailService:
    def __init__(self):
        self.email_address = None
        self.email = None


    def get_email_address(self):
        return self.email

    def send_verification_email(self, request):
        if self.email_address:
            self.email_address.send_confirmation(request)
            return True

        return False


    @staticmethod
    def does_user_already_exist_by_email(user_id, email: str) -> bool:
        return User.objects.filter(email=email).exclude(pk=user_id).exists()


    @staticmethod
    @transaction.atomic
    def change_email(user, new_email: str) -> bool:

        email_address, _ = EmailAddress.objects.update_or_create(
            user=user,
            primary=True,
            defaults={
                "email": new_email,
                "verified": False,
            }
        )

        if email_address.email != new_email:
            return False

        user.email = new_email
        user.save(update_fields=["email"])

        return True


    def is_email_unverified(self, user) -> bool:
        self.email_address = EmailAddress.objects.filter(
            user=user,
            primary=True,
            verified=False,
        ).first()

        if self.email_address:
            self.email = self.email_address.email
            return True

        return False

