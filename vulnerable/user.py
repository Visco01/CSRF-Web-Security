class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class UserRepository:
    def __init__(self, users):
        self.users = users

    def get_by_username(self, username):
        return next(
            (user for user in self.users if user.username == username),
            None,
        )


user_repository = UserRepository(
    [
        User("alice", "123", "alice@gmail.com"),
        User("bob", "456", "bob@gmail.com"),
    ]
)
