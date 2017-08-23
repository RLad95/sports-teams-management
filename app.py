from flask import Flask
from controllers.city import city_url
from controllers.player import player_url
from controllers.user import user_url
from controllers.jsonendpoints import json_url
from flask_sqlalchemy import SQLAlchemy
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

app.register_blueprint(city_url)
app.register_blueprint(player_url)
app.register_blueprint(user_url)
app.register_blueprint(json_url)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':

    db.init_app(app)
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)