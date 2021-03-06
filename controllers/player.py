from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask import session as login_session

from models.city import City
from models.player import Player

player_url = Blueprint('player_url', __name__)


@player_url.route('/city/<int:city_id>/')
@player_url.route('/city/<int:city_id>/players/')
def show_players(city_id):
    city = City.find_by_id(city_id)
    players = Player.find_all_players(city_id)
    if 'username' not in login_session:
        return render_template('public_players.html', players=players, city=city)
    else:
        return render_template('players.html', players=players, city=city)


# Add a new Player to the city
@player_url.route('/city/<int:city_id>/players/new/', methods=['GET', 'POST'])
def new_player(city_id):
    if 'username' not in login_session:
        return redirect('/login')
    city = City.find_by_id(city_id)
    if city.user_id != login_session['user_id']:
        flash('You are not authorized to add new players to the city')
        return redirect(url_for('player_url.show_players', city_id=city_id))
    if request.method == 'POST':
        new_player_figure = Player(name=request.form['name'], height=request.form[
                           'height'], weight=request.form['weight'], sport=request.form['sport'], city_id=city_id)
        if new_player_figure.name == '':
            flash('Please enter a name before submitting') # flash if the field is empty
            return render_template('new_player.html', city_id=city_id)
        new_player_figure.save_to_db()
        flash('New Player %s Successfully Created' % (new_player_figure.name))
        return redirect(url_for('player_url.show_players', city_id=city_id))
    else:
        return render_template('new_player.html', city_id=city_id)


# Edit player from different players
@player_url.route('/city/<int:city_id>/players/<int:player_id>/edit', methods=['GET', 'POST'])
def edit_player(city_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    city = City.find_by_id(city_id)
    if city.user_id != login_session['user_id']:
        flash('You are not authorized to edit players in the city')
        return redirect(url_for('player_url.show_players', city_id=city_id))
    edited_player_figure = Player.find_by_id(player_id)
    if request.method == 'POST':
        if request.form['name']:
            edited_player_figure.name = request.form['name']
        if request.form['height']:
            edited_player_figure.height = request.form['height']
        if request.form['weight']:
            edited_player_figure.weight = request.form['weight']
        if request.form['sport']:
            edited_player_figure.sport = request.form['sport']
        edited_player_figure.save_to_db()
        flash('Player Successfully Edited')
        return redirect(url_for('player_url.show_players', city_id=city_id))
    else:
        return render_template('edit_player.html', city_id=city_id, player_id=player_id, player=edited_player_figure)


# Delete players
@player_url.route('/city/<int:city_id>/players/<int:player_id>/delete', methods=['GET', 'POST'])
def delete_player(city_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    city = City.find_by_id(city_id)
    if city.user_id != login_session['user_id']:
        flash('You are not authorized to delete players in the city')
        return redirect(url_for('player_url.show_players', city_id=city_id))
    player_to_delete = Player.find_by_id(player_id)
    if request.method == 'POST':
        player_to_delete.delete_from_db()
        flash('Player Successfully Deleted')
        return redirect(url_for('player_url.show_players', city_id=city_id))
    else:
        return render_template('delete_player.html', player=player_to_delete)
