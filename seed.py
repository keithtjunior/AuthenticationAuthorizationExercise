from models import db, User, Feedback
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Feedback.query.delete()
