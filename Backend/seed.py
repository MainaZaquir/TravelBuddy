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

        db.session.commit()

if __name__ == '__main__':
    seed_database()
