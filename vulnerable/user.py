class User:
    def __init__(self, username, password, secret):
        self.username = username
        self.password = password
        self.secret = secret


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
        User("alice", "123", "15_th15_th3_r34l_l1f3"),
        User("bob", "456", "15_th15_ju57_f4nt45y"),
    ]
)
