from flask import Flask, request, jsonify
from config import Config  
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)  
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Definining database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    dates = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Trip(id={self.id}, destination={self.destination}, dates={self.dates}, description={self.description})>"

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
    trips = Trip.query.all()
    trip_list = [{'id': trip.id, 'destination': trip.destination, 'dates': trip.dates, 'description': trip.description} for trip in trips]
    return jsonify({'trips': trip_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
