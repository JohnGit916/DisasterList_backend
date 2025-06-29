from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from extensions import db, jwt_blacklist
from models.user import User

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'error': 'All fields are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 409
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already registered'}, 409

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        # ✅ Ensure identity is a string
        token = create_access_token(identity=str(user.id))
        return {'access_token': token, 'username': user.username}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {'error': 'Invalid credentials'}, 401

        # ✅ Ensure identity is a string
        token = create_access_token(identity=str(user.id))
        return {'access_token': token, 'username': user.username}, 200

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        jwt_blacklist.add(jti)
        return {'message': 'Successfully logged out'}, 200
