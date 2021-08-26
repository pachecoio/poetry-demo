from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from api.blueprints import blueprint
from flask_marshmallow import Marshmallow
from api.database import setup_db

__version__ = "0.1.0"

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    Marshmallow(app)
    app.db = setup_db(app)
    Migrate(app=app, db=app.db)
    app.register_blueprint(blueprint)
    app.debugger_active = False

    return app
