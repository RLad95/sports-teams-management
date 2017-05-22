from database import db
from user import Users


class City(db.model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

    @classmethod
    def find_all_cities(cls):
        return cls.query.order_by(asc(cls.name)).all()

    @classmethod
    def find_by_id(cls, city_id):
        return cls.query.filter_by(id=city_id).first()
