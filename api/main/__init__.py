from flask import Blueprint

api = Blueprint('api', __name__)

from api.main import routes