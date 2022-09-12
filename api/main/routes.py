from flask import request, jsonify, Blueprint
from api import current_app
from api.models import User
from api import db


@api.route('/')
@api.route('/index')
def index():
    return jsonify( {'msg' : 'hello'} )

