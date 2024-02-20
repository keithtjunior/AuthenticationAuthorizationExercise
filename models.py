"""Models for Feedback"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    feedback = db.relationship('Feedback', backref="user", cascade='all, delete')

    def __repr__(self):
        u = self
        return f'<User username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>'
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register and return new user w/ hashed password"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate and return true if user exists & password is correct, else return false"""
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, pwd):
                return {'valid': True, 'user': user, 'message': None}
            else:
                return {'valid': False, 'user': None, 'message': 'password'}
        else:
            return {'valid': False, 'user': None, 'message': 'username'}
        

class Feedback(db.Model):
    """Feedback"""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)