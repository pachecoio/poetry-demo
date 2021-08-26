from poetry_demo.repositories import BaseRepository
from poetry_demo.models.user_models import User


class UserRepository(BaseRepository):
    name = "User"
    model = User