from flask_sqlalchemy import SQLAlchemy
from aldo_safaris.extensions import db

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact=db.Column(db.Integer,unique=True)
    password = db.Column(db.String(128), nullable=False)
    bookings = db.relationship('Booking', backref='user')
    car_hiring = db.relationship('Car', backref='user')
    
    def __init__(self,user_name,email,password,contact):
        self.user_name=user_name
        self.email= email
        self.contact= contact
        self.password=password
   

    def __repr__(self):
        return '<User %r>' % self.username
    

