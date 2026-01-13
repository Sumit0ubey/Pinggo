from channels.db import database_sync_to_async

from chats.models import GroupMessage


class MessageService:

    """
    # don't touch it, it works with consumer.

    Before making any changes, please check does it break consumer.
    Remember 'Me'

    # DON'T TOUCH IT, IT WORKS WITH CONSUMER
    """

    @staticmethod
    async def get_message(message_id):
        return await database_sync_to_async(GroupMessage.objects.select_related("author").get)(
            id=message_id
        )


    @staticmethod
    async def create_message(user, group, message):
        return await database_sync_to_async(GroupMessage.objects.create)(
            message=message,
            author=user,
            group=group,
        )

    @staticmethod
    def create_message_upload(user, group, message, file_url, file_type, file_name):
        return GroupMessage.objects.create(
            group=group,
            author=user,
            message=message,
            file_url=file_url,
            file_type=file_type,
            file_name=file_name,
        )
