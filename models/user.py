from base import Base
from database import db


class User(Base):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))

    def __init__(self, name, email, picture):
        self.name = name
        self.email = email
        self.picture = picture

    @property
    def serialize(self):
        self.email_ = {'id': self.id, 'name': self.name, 'email': self.email, }
        return self.email_

    @classmethod
    def get_user_id(cls, email):
        try:
            user = cls.query.filter_by(email=email).one()
            return user.id
        except:
            return None

    @classmethod
    def find_user_by_id(cls, user_id):
        try:
            user = cls.query.filter_by(id=user_id).one()
            return user
        except:
            return None

    @classmethod
    def get_user_info(cls, email):
        try:
            user = cls.query.filter_by(email=email).one()
            return user
        except:
            return None