from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import mimetypes

class Command(BaseCommand):
    help = "Migrate local media files to Cloudinary"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting media migration...")

        from users.models import Profile
        from chats.models import ChatGroup, GroupMessage

        for profile in Profile.objects.exclude(image=""):
            self.migrate(profile, "image", "avatar")

        for group in ChatGroup.objects.exclude(image=""):
            self.migrate(group, "image", "chat/images")

        for msg in GroupMessage.objects.exclude(file=""):
            self.migrate(msg, "file", "chat/files")

        self.stdout.write(self.style.SUCCESS("Finished media migration 🎉"))

    def migrate(self, instance, field_name, _unused=None):
        field = getattr(instance, field_name)

        if not field or field.name.startswith(("http://", "https://")):
            return

        local_path = Path(settings.MEDIA_ROOT) / field.name

        if not local_path.exists():
            self.stdout.write(
                self.style.WARNING(f"Missing: {field.name}")
            )
            return

        mime, _ = mimetypes.guess_type(str(local_path))

        try:
            with local_path.open("rb") as f:
                django_file = File(f)

                if mime:
                    if mime.startswith("image"):
                        django_file.resource_type = "image"
                    elif mime.startswith("video"):
                        django_file.resource_type = "video"
                    else:
                        django_file.resource_type = "raw"
                else:
                    django_file.resource_type = "raw"

                field.save(field.name, django_file, save=True)

            self.stdout.write(self.style.SUCCESS(f"Uploaded → {field.name}"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed {field.name}: {e}")
            )
