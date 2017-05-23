from flask import Blueprint, jsonify

from models.city import City
from models.player import Player


json_url = Blueprint('json_url', __name__)


@json_url.route('/city/<int:city_id>/players/JSON')
def players_json(city_id):
    players = Player.find_all_players(city_id)
    return jsonify(players=[i.serialize for i in players])


@json_url.route('/city/<int:city_id>/players/<int:player_id>/JSON')
def single_player_json(player_id):
    player_figure = Player.find_by_id(player_id)
    return jsonify(player=player_figure.serialize)


@json_url.route('/city/JSON')
def cities_json():
    cities = City.find_all_cities()
    return jsonify(cities=[c.serialize for c in cities])