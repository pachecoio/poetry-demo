from flask_restful import Resource
from flask import jsonify
from poetry_demo.repositories.user_repository import UserRepository
from poetry_demo.helpers.decorators import marshal_with, parse_with
from poetry_demo.schemas.user_schemas import UserSchema, UserCreateSchema
from poetry_demo.models import User


class UserCollectionResource(Resource):
    def __init__(self, repository_factory=UserRepository):
        self.repository = repository_factory()

    @marshal_with(UserSchema(many=True))
    def get(self):
        return self.repository.filter().all()

    @parse_with(UserCreateSchema())
    @marshal_with(UserSchema())
    def post(self, entity=None):
        return self.repository.insert(**entity)