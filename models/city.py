from base import Base
from user import User
from database import db


class City(Base):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

    @classmethod
    def find_all_cities(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def find_by_id(cls, city_id):
        return cls.query.filter_by(id=city_id).first()
