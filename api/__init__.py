from sys import prefix
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
babel = Babel()

def create_api(config_class=Config):
  api = Flask(__name__)
  api.config.from_object(config_class)
  db.init_app(api)
  migrate.init_app(api, db)
  babel.init_app(api)
  CORS(api)

  from api.errors import bp as errors_bp
  api.register_blueprint(errors_bp)

  from api.api import bp as api_bp
  api.register_blueprint(api_bp, url_prefix='/api')

  from api.main import api as main_bp
  api.register_blueprint(main_bp, prefix=('/'))

  from api.auth import bp as auth_bp
  api.register_blueprint(auth_bp, url_prefix='/auth')

  return api

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from api.models import  models

