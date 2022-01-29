import sqlalchemy
from data.models.base import db


class Cat(db.Model):
    __tablename__ = 'cats'
    catId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(100), nullable=False)
    images = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.VARCHAR(2000), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f'Cat {self.name}'
