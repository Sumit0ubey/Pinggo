from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ChatGroup(models.Model):
    CHAT_TYPES = (
        ("global", "Global"),
        ("group", "Group"),
        ("private", "Private"),
    )

    group_name = models.CharField(max_length=255, unique=True, db_index=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default="global")
    description = models.TextField(max_length=350, blank=True)
    image = models.ImageField(upload_to='chats/images', blank=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="created_chats"
    )

    members = models.ManyToManyField(
        User,
        related_name="chat_groups",
        blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.group_name

    def clean(self):
        if self.chat_type == "private" and self.pk:
            if self.members.count() != 2:
                raise ValidationError("Private chat must have exactly 2 members.")

        if self.chat_type == "global" and self.members.exists():
            raise ValidationError("Global chat should not have members.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.chat_type in ["group", "private"]:
            self.members.add(self.creator)

    def is_active(self, active_chat):
        return active_chat is not None and self.id == active_chat.id

    def is_owner(self, user):
        return self.creator == user

    def can_edit(self, user):
        return self.creator == user

    def can_view(self, user):
        if self.chat_type == "global":
            return True
        return self.members.filter(id=user.id).exists()

    def display_name_for(self, user):

        if self.chat_type == "private":
            parts = self.group_name.replace("_", "-").split("-")

            for part in parts:
                if part != user.username:
                    return part.replace("-", " ").title()

            return self.group_name

        prefix = f"{self.creator.username}-"
        name = self.group_name

        if name.startswith(prefix):
            name = name[len(prefix):]

        return name.replace("_", " ").replace("-", " ").title()

    @property
    def display_name(self):
        prefix = f"{self.creator.username}-"
        if self.group_name.startswith(prefix):
            return self.group_name[len(prefix):].replace('_', ' ').replace('-', ' ').title()
        return self.group_name.replace('_', ' ').replace('-', ' ').title()

    @property
    def pic(self):
        if self.image:
            return self.image.url
        return static("images/group.svg")


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.author}: {self.message}'

    class Meta:
        ordering = ['-created_at']
