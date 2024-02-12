from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config  
from flask_sqlalchemy import SQLAlchemy
from models import Trip, User, Request, db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_buddy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True
migrate = Migrate(app, db)

db.init_app(app)

# Profile endpoint
@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    if request.method == 'GET':
        # Fetching the user profile
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'username': user.username,
                'email': user.email
            }), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    elif request.method == 'PUT':
        # Updating the user profile
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        if user:
            # Updating the user attributes
            user.username = request.json.get('username', user.username)
            user.email = request.json.get('email', user.email)
            db.session.commit()
            return jsonify({'message': 'User profile updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404

# Changing the password endpoint
@app.route('/change-password', methods=['PUT'])
def change_password():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        new_password = request.json.get('new_password')
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Trips endpoint
@app.route('/trips', methods=['GET'])
def get_trips():
    trips = []
    for trip in Trip.query.all():
            trip_dict = {'id': trip.id, 'destination': trip.destination, 'start_date ': trip.start_date , 'description': trip.description}
    # trips = Trip.query.all()
    trip.append(trip_dict)

    response = make_response(
        jsonify(),
        200,
    )
    return response
    # trip_list = [{'id': trip.id, 'destination': trip.destination, 'start_date ': trip.start_date , 'description': trip.description} for trip in trips]
    # return jsonify(Trip_dict), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)
