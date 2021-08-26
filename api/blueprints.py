from flask import Blueprint
from flask_restful import Api
from poetry_demo.resources.user_resources import UserCollectionResource

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(UserCollectionResource, "/user")
