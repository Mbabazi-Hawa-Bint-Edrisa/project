from flask_sqlalchemy import SQLAlchemy
from aldo_safaris.extensions import db

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'))
    payment_date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))
    car_id = db.Column(db.Integer, db.ForeignKey('rentals.car_id'))

    booking = db.relationship('Booking', backref='payments')
    car_hiring = db.relationship('Rental', backref='payments')
    
    

def __repr__(self):
    return '<Payment %r>' % self.payment_id

   