from flask import jsonify
from api import db
from api.api import bp
from api.api.auth import basic_auth, token_auth

# View function decorated with basic_auth.login_required decorator from
# the HTTPBasicAuth instance, instruct Flask-HHTPAuth to verify authentication
# This views get_token function reiles on the get_token method in the User model
# which will produce a token, then a db commit is issued with the expiration added to
# the db.

# Get a token
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({ 'token' : token })

# DELETE request to revoke token
@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204