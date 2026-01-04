def private_room_name(user1, user2):
    usernames = sorted([user1.username, user2.username])
    return f"{usernames[0]}-{usernames[1]}"
