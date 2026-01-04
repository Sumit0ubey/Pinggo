
"""
For Testing only  (Used Initially when redis cache was not initialized)
"""

# class Presence:
#     online_users_id = set()
#
#     @classmethod
#     def get_presence(cls):
#         return len(cls.online_users_id) if len(cls.online_users_id) > 0 else 1
#
#     @classmethod
#     def increase_presence(cls, id):
#         cls.online_users_id.add(id)
#
#     @classmethod
#     def decrease_presence(cls, id):
#         cls.online_users_id.discard(id)


from django_redis import get_redis_connection


class Presence:
    redis = get_redis_connection("default")

    @staticmethod
    def key(chat_type, chat_name):
        return f"presence:{chat_type}:{chat_name}"

    @classmethod
    def add(cls, chat_type, chat_name, user_id):
        cls.redis.sadd(cls.key(chat_type, chat_name), user_id)

    @classmethod
    def remove(cls, chat_type, chat_name, user_id):
        cls.redis.srem(cls.key(chat_type, chat_name), user_id)

    @classmethod
    def count(cls, chat_type, chat_name):
        return cls.redis.scard(cls.key(chat_type, chat_name))