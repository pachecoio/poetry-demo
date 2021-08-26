from flask import Blueprint
from flask_restful import Api

from api.resources.user_resources import UserCollectionResource

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(UserCollectionResource, "/user")
