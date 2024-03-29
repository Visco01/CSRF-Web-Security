from .user import User

class Post:
    def __init__(self, title, desc, user):
        self.title = title
        self.desc = desc
        self.user = user

class PostRepository:
    def __init__(self, posts):
        self.posts = posts

    def get_by_title(self, title):
        return next(
            (post for post in self.posts if post.title == title),
            None,
        )

    def add_post(self, post):
        self.posts.append(post)

post_repository = PostRepository(
    [
        Post("First Post", "This is the first post", User("alice", "123", "15_th15_th3_r34l_l1f3")),
        Post("Second Post", "This is the second post", User("bob", "456", "15_th15_ju57_f4nt45y")),
    ]
)
