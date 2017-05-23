from base import Base
from city import City
from database import db


class Player(Base):
    __tablename__ = 'player'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(250))
    height = db.Column(db.Integer)  # in cm
    weight = db.Column(db.Integer)  # in kg
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship(City)

    def __init__(self, name, height, weight, sport, city_id):
        self.name = name
        self.height = height
        self.weight     = weight
        self.sport = sport
        self.city_id = city_id

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'height': self.height,
            'weight': self.weight,
            'sport': self.sport,
        }

    @classmethod
    def find_all_players(cls, city_id):
        return cls.query.filter_by(city_id=city_id).all()

    @classmethod
    def find_by_id(cls, player_id):
        return cls.query.filter_by(id=player_id).first()

