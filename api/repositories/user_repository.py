from api.repositories import BaseRepository
from api.models.user_models import User


class UserRepository(BaseRepository):
    name = "User"
    model = User