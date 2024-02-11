from app import app, db
from models import User, Trip, Request  # Import all models here
from datetime import datetime

def seed_database():
    with app.app_context():
        # Create database schema using Flask-Migrate
        db.create_all()

        # Create some users with unique usernames and emails
        users_data = [
            {'username': 'uniqe_user011', 'password': 'password11', 'email': 'uniqe_user011@example.com'},
            {'username': 'uniqe_user102', 'password': 'password12', 'email': 'uniqe_user102@example.com'},
            {'username': 'uniqe_user13', 'password': 'password13', 'email': 'uniqe_user13@example.com'}
        ]

        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)

        # Commit users to the database
        db.session.commit()

        # Create sample trips
        trips_data = [
            {'name': 'Trip to Paris', 'destination': 'Paris', 'start_date': datetime.strptime('2024-02-15', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-02-20', '%Y-%m-%d'), 'user_id': 1},
            {'name': 'Weekend Getaway', 'destination': 'Beach', 'start_date': datetime.strptime('2024-03-10', '%Y-%m-%d'), 'end_date': datetime.strptime('2024-03-12', '%Y-%m-%d'), 'user_id': 2}
        ]

        for trip_data in trips_data:
            trip = Trip(**trip_data)
            db.session.add(trip)

        # Commit trips to the database
        db.session.commit()

        # Create sample requests
        requests_data = [
            {'user_id': 1, 'trip_id': 2, 'status': 'approved'},
            {'user_id': 2, 'trip_id': 1, 'status': 'pending'}
        ]

        for request_data in requests_data:
            request = Request(**request_data)
            db.session.add(request)

        # Commit requests to the database
        db.session.commit()

if __name__ == '__main__':
    seed_database()
