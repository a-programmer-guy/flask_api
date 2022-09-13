from api import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
from datetime import datetime, timedelta
import os
from flask import session, url_for

# Task class will represent tasks written by users.
# user_id field initialized as a foreign key to user.id
# User class has a new tasks field, that is initialized with db.relationship.
# This is not an actual database field, but a high-level view of the
# relationship between users and tasks.
# backref argument defines the name of a field that will be added to the
# objects of the "many" class that points back at the "one" object.
# This will add a post.author expression that will return the user given a post
# Token field added to User model to support authentication
# 3 methods to work with tokens: get_token, revoke_token, check_token
# PaginatedAPIMixin can be used for paginated requests of collection from the client
class PaginatedAPIMixin(object):
  @staticmethod
  def to_collection_dict(query, page, per_page, endpoint, **kwargs):
    resources = query.paginate(page, per_page, False)
    data = {
      'items': [item.to_dict() for item in resources.items],
      '_meta': {
        'page': page,
        'per_page': per_page,
        'total_pages': resources.pages,
        'total_items': resources.total
      },
      '_links': {
        'self': url_for(endpoint, page=page, per_page=per_page,
                        **kwargs),
        'next': url_for(endpoint, page=page + 1, per_page=per_page,
                        **kwargs) if resources.has_next else None,
        'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                        **kwargs) if resources.has_prev else None
      }
    }
    return data

class User(PaginatedAPIMixin, UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  tasks = db.relationship('Task', backref='author', lazy='dynamic')
  token = db.Column(db.String(32), index=True, unique=True)
  token_expiration = db.Column(db.DateTime)

  # Return username object
  def __repr__(self):
      return '<User {}>'.format(self.username)

  # Generate a hashed version of the password
  def set_password(self, password):
        self.password_hash = generate_password_hash(password)

  # Check if the hashed password is equal to the password passed in
  def check_password(self, password):
        return check_password_hash(self.password_hash, password)

  # Build a dict object of our user that can be used to send back to client
  def to_dict(self, include_email=False):
    data = {
      'id': self.id,
      'username': self.username,
    }
    if include_email:
      data['email'] = self.email
    return data

  # new_user argument to check if we are registering a new user or updating user
  def from_dict(self, data, new_user=False):
    for field in ['username', 'email']:
      if field in data:
        setattr(self,field, data[field])
      if new_user and 'password' in data:
        self.set_password(data['password'])

  # Helper method to create a token
  # Return a randomized string as a token for the user, encoded in base64
  # Checks if an existing token has more than a minute left and returns it
  def get_token(self, expires_in=3600):
    now = datetime.utcnow()
    if self.token and self.token_expiration > now +timedelta(seconds=60):
      return self.token
    # Create a randomized token - 24 chars long, encoded in base64 so it is readable
    self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    # Set expiration time
    self.token_expiration = now + timedelta(seconds=expires_in)
    # Add token to the user session and return the token
    db.session.add(self)
    return self.token

  # Helper method to revoke token
  # Set expiration date to one second before current time - making token invalid
  def revoke_token(self):
    self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

  # Check if the token exists or has expired - return None if true, return User if valid
  @staticmethod
  def check_token(token):
    user = User.query.filter_by(token=token).first()
    if user is None or user.token_expiration < datetime.utcnow():
      return None
    return user

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(200))
  reminder = db.Column(db.Boolean(), default=False, nullable=False)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
      return '<Post {}>'.format(self.text)
