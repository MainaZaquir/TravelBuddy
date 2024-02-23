import os

from flask import Flask, request, jsonify, make_response, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Trip, User, db
from datetime import datetime

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../frontend/build',
    template_folder='../frontend/build'
)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI", 'postgresql://maina:0ptWCXmgfwvD0eHIaOH4OGU4HAvtM14v@dpg-cnc7mmicn0vc73970aqg-a.frankfurt-postgres.render.com/travelbuddy_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")

@app.route('/')
def home():
    return {"message": "Welcome to the travel API"}

@app.route('/profile/<int:id>', methods=['GET', 'PUT'])
def profile(id):
    if request.method == 'GET':
        # user_id = request.args.get('user_id')
        user = User.query.filter_by(id=id).first()
        if user:
            response_data = {
                'username': user.username,
                'email': user.email
            }
            response = make_response(
                jsonify(response_data), 200
            )
            return response
            # return make_response(jsonify(response_data), 200)
        else:
            return jsonify({'message': 'User not found'}), 404
    elif request.method == 'PUT':
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        if user:
            user.username = request.json.get('username', user.username)
            user.email = request.json.get('email', user.email)
            db.session.commit()
            return jsonify({'message': 'User profile updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Please provide username, email, and password'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User signed up successfully'}), 201


@app.route('/change-password', methods=['PUT'])
def change_password():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        new_password = request.json.get('new_password')
        # user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/trips', methods=['GET'])
def get_trips():
    trips = []
    for trip in Trip.query.all():
        trip_dict = {
            'id': trip.id,
            'destination': trip.destination,
            'start_date ': trip.start_date,
            'name': trip.name,
            'end_date': trip.end_date
        }
        trips.append(trip_dict)
    db.session.commit()

    response = make_response(
        jsonify(trips),
        200,
    )
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5555)
