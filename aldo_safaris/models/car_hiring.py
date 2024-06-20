from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Car Model 
class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255), nullable=True)
    price_per_day = db.Column(db.Float, nullable=False)  # New field for daily rental price

    rentals = db.relationship('Rental', backref='car')

    def __repr__(self):
        return f'<Car {self.make} {self.model} >'

# Rental Model
class Rental(db.Model):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)  # New field for total rental cost

    def __repr__(self):
        return f'<Rental {self.id} - {self.car}>'
