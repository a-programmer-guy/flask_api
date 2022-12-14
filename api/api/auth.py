from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from api.models.models import User
from api.api.errors import error_response

# HTTPBasicAuth implements the basic authentication flow
basic_auth = HTTPBasicAuth()

# HTTPTokenAuth is used to protect our routes with tokens
token_auth = HTTPTokenAuth()

# username and password recieved as arguments
# Returns authenticated user if valid, None if credentials aren't valid
# Authenticated user available in the api as basic_auth.current_user()
@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

# error_response is generated by the error_response() function in errors.py
# Returns HTTP status of 401 for Unauthorized error.
@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

# the token is recieved as an argument
# verify_token decorated function uses User.check_token function to return
# the token if its valid, else None is returned and client is rejected
@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)