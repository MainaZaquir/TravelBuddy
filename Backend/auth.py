import os
import sys
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import User, BlacklistedToken
from datetime import timedelta

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(parent_dir)

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

auth_bp.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return BlacklistedToken.query.filter_by(jti=jti).first() is not None
