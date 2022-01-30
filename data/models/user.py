import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.models.base import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    fullname = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.VARCHAR, primary_key=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User {self.username}'
