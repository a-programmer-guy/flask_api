from flask import Blueprint

bp = Blueprint('auth_bp', __name__)

from api.auth import routes