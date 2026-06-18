from app import db
from flask_login import UserMixin
from app import login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="student")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))