from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post

@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f""

@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f""

@dataclass
class Discord(Paysite):
    """
    TODO: finish links.
    """
    name: str = 'discord'
    title: str = 'Discord'
    user: User = User()
    post: Post = Post()
