from api import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Task class will represent tasks written by users.
# user_id field initialized as a foreign key to user.id
# User class has a new tasks field, that is initialized with db.relationship.
# This is not an actual database field, but a high-level view of the
# relationship between users and tasks.
# backref argument defines the name of a field that will be added to the
# objects of the "many" class that points back at the "one" object.
# This will add a post.author expression that will return the user given a post

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  tasks = db.relationship('Task', backref='author', lazy='dynamic')

  def __repr__(self):
      return '<User {}>'.format(self.username)

  def set_password(self, password):
        self.password_hash = generate_password_hash(password)

  def check_password(self, password):
        return check_password_hash(self.password_hash, password)

  # Build a dict object of our user to send back to client
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
