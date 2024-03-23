from flask import Flask
from flask_restx import Api
from models import User, Recipe
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipes_ns
from auth import auth_ns
from flask_cors import CORS

def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    CORS(app)

    migrate=Migrate(app,db)
    JWTManager(app)

    api=Api(app)

    api.add_namespace(auth_ns)
    api.add_namespace(recipes_ns)
        
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Recipe": Recipe,
            "User": User
        }
    
    return app