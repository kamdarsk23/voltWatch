from flask import request,make_response
from flask_restx import Resource,Namespace,fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token,create_refresh_token,
                                jwt_required, get_jwt_identity)

auth_ns=Namespace('auth',description="A namespace for our authentication")

signup_model=auth_ns.model (
    "SignUp",
    {
        "name":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model=auth_ns.model (
    "LogIn",
    {
        "email":fields.String(),
        "password":fields.String()
    }
)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data=request.get_json()

        db_user=User.query.filter_by(email=data.get("email")).first()
        if db_user is not None:
            return {"message":"account with email already exists"},400

        new_user=User(
            name=data.get("name"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )
        new_user.save()

        return {"message":"user created successfully"},201
    
@auth_ns.route('/login')
class LogIn(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data=request.get_json()
        email=data.get('email')
        password=data.get('password')
        db_email=User.query.filter_by(email=email).first()
        if db_email and check_password_hash(db_email.password,password):
            access_token=create_access_token(identity=db_email.email)
            refresh_token=create_refresh_token(identity=db_email.email)

            return {"access token":access_token, "refresh token": refresh_token}

@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_access_token=create_access_token(identity=current_user)

        return make_response({"access token":new_access_token}),200