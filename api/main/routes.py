from flask import request, jsonify, Blueprint, current_app
from api.models.models import User
from api import db
from api.main import api



@api.route('/')
@api.route('/index')
def index():
    return jsonify( {'msg' : 'hello'} )

@api.route('/register')
def register():
    data = request.get_json() or {}

    new_user=User(
        username = data.get('username'),
        email = data.get('email'),
        password = data.get('password')
    )

