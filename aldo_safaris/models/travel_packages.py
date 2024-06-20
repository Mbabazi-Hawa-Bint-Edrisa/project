from flask_sqlalchemy import SQLAlchemy
from aldo_safaris.extensions import db

db = SQLAlchemy()

class TravelPackage(db.Model):
    __tablename__ = 'TravelPackages'

    package_id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    destinations = db.Column(db.ARRAY(db.String(100)))
    activities = db.Column(db.ARRAY(db.String(100)))
    inclusions = db.Column(db.Text)
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    image_url = db.Column(db.String(200))
    
    booking = db.relationship('Booking', backref='TravelPackages')
    

    def __repr__(self):
        return '<TravelPackage %r>' % self.package_name
