from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from aldo_safaris.extensions import db, migrate, jwt, bcrypt
from aldo_safaris.controllers.booking_controller import booking_bp 
from aldo_safaris.controllers.payments_controller import payment_bp
from aldo_safaris.controllers.car_hiring_controller import car_rental_bp 
from aldo_safaris.controllers.notifications_controller import notification_bp
from aldo_safaris.controllers.t_package_controller import travel_package_bp
from aldo_safaris.controllers.user_accounts_controller import customer
from aldo_safaris.models.user_accounts import User
from aldo_safaris.models.booking import Booking
from aldo_safaris.models.car_hiring import Car, Rental
from aldo_safaris.models.notifications import Notification
from aldo_safaris.models.payments import Payment
from aldo_safaris.models.travel_packages import TravelPackage

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(booking_bp, url_prefix='/api/v1/booking')
    app.register_blueprint(car_rental_bp, url_prefix='/api/v1/car_rental')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')
    app.register_blueprint(payment_bp, url_prefix='/api/v1/payment')
    app.register_blueprint(travel_package_bp, url_prefix='/api/v1/travel_package')
    app.register_blueprint(customer, url_prefix='/api/v1/customer')

    # Ensure models are registered with SQLAlchemy
    with app.app_context():
        db.create_all()  # Create all database tables (if not created)

    return app
