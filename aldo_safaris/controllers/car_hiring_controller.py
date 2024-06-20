from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime
from aldo_safaris.extensions import db
from aldo_safaris.models.car_hiring import Car, Rental

# Define the blueprint
car_rental_bp = Blueprint('car_rental', __name__, url_prefix='/api/v1')

# Allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Car Management Routes
@car_rental_bp.route('/car', methods=['POST'])
@jwt_required()
def create_car():
    try:
        # Extract car data from request
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        price_per_day = request.form.get('price_per_day')
        file = request.files.get('image')

        # Basic input validation
        if not all([make, model, year, price_per_day]):
            return jsonify({"error": "Make, model, year, and price per day are required"}), 400
        
        # Validate that price_per_day is a float
        try:
            price_per_day = float(price_per_day)
        except ValueError:
            return jsonify({"error": "Price per day must be a valid number"}), 400

        # Validate and save the image if provided
        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            image_url = os.path.join(current_app.config['UPLOAD_URL'], filename)

        # Create a new car
        new_car = Car(
            make=make,
            model=model,
            year=year,
            available=True,
            image_url=image_url,
            price_per_day=price_per_day  # Save the price per day
        )

        # Add car to the database and commit
        db.session.add(new_car)
        db.session.commit()

        return jsonify({'message': 'Car created successfully', 'car_id': new_car.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@car_rental_bp.route('/car/<int:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    try:
        # Get car by ID
        car = Car.query.get(car_id)

        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Extract car data from request
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        price_per_day = request.form.get('price_per_day')
        file = request.files.get('image')

        # Update car fields if provided in request
        if make:
            car.make = make
        if model:
            car.model = model
        if year:
            car.year = year
        if price_per_day:
            try:
                car.price_per_day = float(price_per_day)
            except ValueError:
                return jsonify({"error": "Price per day must be a valid number"}), 400

        # Validate and save the new image if provided
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            car.image_url = os.path.join(current_app.config['UPLOAD_URL'], filename)

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Car updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rental Management Route
@car_rental_bp.route('/rental', methods=['POST'])
@jwt_required()
def create_rental():
    try:
        # Extract rental data from request
        car_id = request.form.get('car_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        user_id = get_jwt_identity()  # Assuming user_id is retrieved from JWT

        # Basic input validation
        if not all([car_id, start_date, end_date]):
            return jsonify({"error": "Car ID, start date, and end date are required"}), 400

        # Convert dates to datetime objects
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date >= end_date:
                return jsonify({"error": "End date must be after start date"}), 400
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Get the car by ID
        car = Car.query.get(car_id)
        if not car:
            return jsonify({"error": "Car not found"}), 404

        # Calculate the total cost
        days_rented = (end_date - start_date).days
        total_cost = days_rented * car.price_per_day

        # Create a new rental
        new_rental = Rental(
            car_id=car.id,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            total_cost=total_cost
        )

        # Add rental to the database and commit
        db.session.add(new_rental)
        db.session.commit()

        return jsonify({'message': 'Rental created successfully', 'rental_id': new_rental.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
