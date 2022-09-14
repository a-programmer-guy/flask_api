from flask import Blueprint

api = Blueprint('main', __name__)

from api.main import routes