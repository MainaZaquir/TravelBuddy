from app import app, db
from models import User, Trip, Request  # Import all models here

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


