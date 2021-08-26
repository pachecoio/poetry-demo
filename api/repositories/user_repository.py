from api.models.user_models import User
from api.repositories import BaseRepository


class UserRepository(BaseRepository):
    name = "User"
    model = User
