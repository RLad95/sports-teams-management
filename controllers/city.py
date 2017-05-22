from flask import render_template, redirect, request, url_for, flash, Blueprint
from models.city import City
from models.user import User
from user import login_session


city_url = Blueprint('city_url', __name__)


# show all cities
@city_url.route('/')
@city_url.route('/city/')
def show_cities():
    cities = City.find_all_cities()
    creator = User.get_user_info(login_session.get('email'))
    if 'username' not in login_session:
        return render_template('public_cities.html', cities=cities, creator=creator)
    else:
        return render_template('cities.html', cities=cities, creator=creator)


# Add a new City
@city_url.route('/city/new/', methods=['GET', 'POST'])
def new_city():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_city = City(name=request.form['name'], user_id=login_session['user_id'])
        new_city.save_to_db()
        flash('New City %s Successfully Created' % new_city.name)
        return redirect(url_for('city_url.show_cities'))
    else:
        return render_template('new_city.html')


# Edit a City
@city_url.route('/city/<int:city_id>/edit', methods=['GET', 'POST'])
def edit_city(city_id):
    if 'username' not in login_session:
        return redirect('/login')
    edited_city = City.find_by_id(city_id)
    if edited_city.user_id != login_session['user_id']:
        flash('You are not authorized to edit the the city.')
        return redirect(url_for('city_url.show_cities'))
    if request.method == 'POST':
        if request.form['name']:
            edited_city.name = request.form['name']
            edited_city.save_to_db()
            flash('City Successfully Edited %s' % edited_city.name)
            return redirect(url_for('city_url.show_cities'))
    else:
        return render_template('edit_city.html', city=edited_city)


# Delete a City
@city_url.route('/city/<int:city_id>/delete/', methods=['GET', 'POST'])
def delete_city(city_id):
    city_to_delete = City.find_by_id(city_id)
    if 'username' not in login_session:
        return redirect('/login')
    if city_to_delete.user_id != login_session['user_id']:
        flash('You are not authorized to delete the city.')
        return redirect(url_for('city_url.show_cities'))
    if request.method == 'POST':
        city_to_delete.delete_from_db()
        flash('%s Successfully Deleted' % city_to_delete.name)
        return redirect(url_for('city_url.show_cities', city_id=city_id))
    else:
        return render_template('delete_city.html', city=city_to_delete)
