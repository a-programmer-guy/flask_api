from flask import request, jsonify, Blueprint, current_app
from api.models.models import User
from api import db
from api.main import api



@api.route('/')
@api.route('/index')
def index():
    return jsonify( {'msg' : 'hello'} )


