
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy, session
from models import Trip, User, Request, db

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_buddy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return {"message": "welcome to the travel API"}
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
        # user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Trips endpoint
@app.route('/trips', methods=['GET'])
def get_trips():
    trips = []
    for trip in Trip.query.all():
        trip_dict = {
            'id': trip.id, 
            'destination': trip.destination, 
            'start_date ': trip.start_date , 
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

from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from models import User, Request, Trip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_buddy.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Blueprint objects
auth_routes = Blueprint('auth_routes', __name__)
user_routes = Blueprint('user_routes', __name__)
request_routes = Blueprint('request_routes', __name__)
trip_routes = Blueprint('trip_routes', __name__)

# Authentication Routes
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid username or password'), 401

@auth_routes.route('/logout')
@jwt_required()
def logout():
    return jsonify(message='Successfully logged out'), 200

# User Routes
@user_routes.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users]), 200
    

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not (username and password and email):
        return jsonify(message='Missing username, password, or email'), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message='Username already exists'), 400

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='User created successfully'), 201

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if username:
        user.username = username
    if password:
        user.password = password
    if email:
        user.email = email

    db.session.commit()
    return jsonify(message='User updated successfully'), 200

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify(message='User deleted successfully'), 200

# Request Routes
@request_routes.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    user_id = data.get('user_id')
    trip_id = data.get('trip_id')
    status = data.get('status')

    if not (user_id and trip_id and status):
        return jsonify(message='Missing user_id, trip_id, or status'), 400

    new_request = Request(user_id=user_id, trip_id=trip_id, status=status)
    db.session.add(new_request)
    db.session.commit()

    return jsonify(message='Request created successfully'), 201

@request_routes.route('/requests', methods=['GET'])
def list_requests():
    requests = Request.query.all()
    return jsonify([{'id': request.id, 'user_id': request.user_id, 'trip_id': request.trip_id, 'status': request.status} for request in requests]), 200

@request_routes.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request_obj = Request.query.get(request_id)
    if request_obj:
        return jsonify({'id': request_obj.id, 'user_id': request_obj.user_id, 'trip_id': request_obj.trip_id, 'status': request_obj.status}), 200
    else:
        return jsonify(message='Request not found'), 404

@request_routes.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    request_obj = Request.query.get(request_id)
    if not request_obj:
        return jsonify(message='Request not found'), 404

    data = request.get_json()
    user_id = data.get('user_id')
    trip_id = data.get('trip_id')
    status = data.get('status')

    if user_id:
        request_obj.user_id = user_id
    if trip_id:
        request_obj.trip_id = trip_id
    if status:
        request_obj.status = status

    db.session.commit()
    return jsonify(message='Request updated successfully'), 200

@request_routes.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request_obj = Request.query.get(request_id)
    if not request_obj:
        return jsonify(message='Request not found'), 404

    db.session.delete(request_obj)
    db.session.commit()
    return jsonify(message='Request deleted successfully'), 200

# Trip Routes
@trip_routes.route('/trips', methods=['POST'])
@jwt_required()
def create_trip():
    data = request.get_json()
    name = data.get('name')
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    user_id = get_jwt_identity()

    if not (name and destination and start_date and end_date):
        return jsonify(message='Missing required fields'), 400

    new_trip = Trip(name=name, destination=destination, start_date=start_date, end_date=end_date, user_id=user_id)
    db.session.add(new_trip)
    db.session.commit()

    return jsonify(message='Trip created successfully'), 201

@trip_routes.route('/trips', methods=['GET'])
@jwt_required()
def list_trips():
    user_id = get_jwt_identity()
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': trip.id, 'name': trip.name, 'destination': trip.destination, 'start_date': str(trip.start_date), 'end_date': str(trip.end_date)} for trip in trips]), 200

@trip_routes.route('/trips/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify(message='Trip not found'), 404

    if trip.user_id != get_jwt_identity():
        return jsonify(message='Unauthorized to access this trip'), 403

    return jsonify({'id': trip.id, 'name': trip.name, 'destination': trip.destination, 'start_date': str(trip.start_date), 'end_date': str(trip.end_date)}), 200

@trip_routes.route('/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify(message='Trip not found'), 404

    if trip.user_id != get_jwt_identity():
        return jsonify(message='Unauthorized to update this trip'), 403

    data = request.get_json()
    trip.name = data.get('name', trip.name)
    trip.destination = data.get('destination', trip.destination)
    trip.start_date = data.get('start_date', trip.start_date)
    trip.end_date = data.get('end_date', trip.end_date)

    db.session.commit()
    return jsonify(message='Trip updated successfully'), 200

@trip_routes.route('/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify(message='Trip not found'), 404

    if trip.user_id != get_jwt_identity():
        return jsonify(message='Unauthorized to delete this trip'), 403

    db.session.delete(trip)
    db.session.commit()
    return jsonify(message='Trip deleted successfully'), 200

# Register blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(request_routes, url_prefix='/request')
app.register_blueprint(trip_routes, url_prefix='/trip')

if __name__ == '__main__':
    app.run(debug=True, port=5555)  






