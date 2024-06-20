from flask_sqlalchemy import SQLAlchemy
from aldo_safaris.extensions import db

#db = SQLAlchemy()

class Booking(db.Model):
    __tablename__ = 'Booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('TravelPackages.package_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date_of_booking = db.Column(db.DateTime)
    travel_start_date = db.Column(db.Date)
    travel_end_date = db.Column(db.Date)
    total_cost = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    booking_status = db.Column(db.String(20))
    destination = db.Column(db.String(100))
    accommodation = db.Column(db.String(100))
    transportation = db.Column(db.String(100))
    activities = db.Column(db.ARRAY(db.String(100)))
    booking_source = db.Column(db.String(20))
  

    travel_package = db.relationship('TravelPackage', backref='Booking')
    user = db.relationship('User', backref='Booking')
    payments = db.relationship('Payment', backref='Booking')
