from app import app, db
from models import User, Trip, Request  # Import all models here

from datetime import datetime

def seed_database():
    with app.app_context():

        db.create_all()
        users_data = [
            {'username': 'Irarah', 'password': 'password11', 'email': 'Irarah011@example.com'},
            {'username': 'Boomer', 'password': 'password12', 'email': 'Boomer102@example.com'},
            {'username': 'Tengen13', 'password': 'password13', 'email': 'Tengen13@example.com'}
        ]

        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit()
        trips_data = [
            {'name': 'Trip to Maldives', 'destination': 'Maldives', 'start_date': datetime.strptime('2024-02-15', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-02-20', '%Y-%m-%d'), 'user_id': 1},
            {'name': 'Weekend Getaway', 'destination': 'Jamiaca', 'start_date': datetime.strptime('2024-03-10', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-03-12', '%Y-%m-%d'), 'user_id': 2},
            {'name': 'Calm Visit', 'destination': 'Spain', 'start_date': datetime.strptime('2024-02-19', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-02-21', '%Y-%m-%d'), 'user_id': 3}
        ]

        for trip_data in trips_data:
            trip = Trip(**trip_data)
            db.session.add(trip)

        db.session.commit()

        requests_data = [
            {'user_id': 1, 'trip_id': 2, 'status': 'approved'},
            {'user_id': 2, 'trip_id': 1, 'status': 'pending'}
        ]

        for request_data in requests_data:
            request = Request(**request_data)
            db.session.add(request)


def seed_database():
    with app.app_context():
        # Create database schema using Flask-Migrate
        db.create_all()

        # Create some users
        user1 = User(username='user1', password='password1', email='user1@example.com')
        user2 = User(username='user2', password='password2', email='user2@example.com')
        db.session.add(user1)
        db.session.add(user2)

        # Commit users to the database
        db.session.commit()

        # Create sample trips
        trip1 = Trip(name='Trip to Paris', destination='Paris', start_date='2024-02-15', end_date='2024-02-20', user_id=user1.id)
        trip2 = Trip(name='Weekend Getaway', destination='Beach', start_date='2024-03-10', end_date='2024-03-12', user_id=user2.id)
        db.session.add(trip1)
        db.session.add(trip2)

        # Commit trips to the database
        db.session.commit()

        # Create sample requests
        request1 = Request(user_id=user1.id, trip_id=trip2.id, status='approved')
        request2 = Request(user_id=user2.id, trip_id=trip1.id, status='pending')
        db.session.add(request1)
        db.session.add(request2)

        # Commit requests to the database

        db.session.commit()

if __name__ == '__main__':
    seed_database()

