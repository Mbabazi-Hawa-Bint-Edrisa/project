from flask import Blueprint, request, jsonify
from datetime import datetime
from aldo_safaris.extensions import db
from aldo_safaris.models.payments import Payment
from aldo_safaris.models.booking import Booking
from flask_jwt_extended import jwt_required, get_jwt_identity

payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/payment')

@payment_bp.route('/', methods=['POST'])
@jwt_required()
def create_payment():
    try:
        # Extract payment data from request JSON
        data = request.json
        
        booking_id = data.get('booking_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        status = data.get('status')

        # Basic input validation
        if not all([booking_id, amount, payment_method, status]):
            return jsonify({"error": "All fields are required"}), 400

        # Verify if the booking exists and belongs to the current user
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        
        if booking.user_id != current_user_id:
            return jsonify({"error": "You are not authorized to add a payment to this booking"}), 403

        # Create a new payment
        new_payment = Payment(
            booking_id=booking_id,
            payment_date=datetime.now(),
            amount=amount,
            payment_method=payment_method,
            status=status
        )

        # Add payment to the database and commit
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Payment created successfully', 'payment_id': new_payment.payment_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    try:
        # Get payment by ID
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        # Ensure the current user is the owner of the booking associated with the payment
        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to view this payment'}), 403

        # Convert payment object to dictionary for response
        payment_data = {
            'payment_id': payment.payment_id,
            'booking_id': payment.booking_id,
            'payment_date': payment.payment_date,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'status': payment.status
        }

        return jsonify(payment_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update_payment(payment_id):
    try:
        # Get payment by ID
        payment = Payment.query.get(payment_id)

        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Ensure the current user is the owner of the booking associated with the payment
        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to update this payment'}), 403

        # Extract payment data from request JSON
        data = request.json

        # Update payment fields if provided in request
        if 'amount' in data:
            payment.amount = data['amount']
        if 'payment_method' in data:
            payment.payment_method = data['payment_method']
        if 'status' in data:
            payment.status = data['status']

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Payment updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    try:
        # Get payment by ID
        payment = Payment.query.get(payment_id)

        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Ensure the current user is the owner of the booking associated with the payment
        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to delete this payment'}), 403

        # Delete payment from the database
        db.session.delete(payment)
        db.session.commit()

        return jsonify({'message': 'Payment deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_payments_for_booking(booking_id):
    try:
        # Verify if the booking exists and belongs to the current user
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        
        if booking.user_id != current_user_id:
            return jsonify({"error": "You are not authorized to view payments for this booking"}), 403

        # Retrieve all payments for the specified booking
        payments = Payment.query.filter_by(booking_id=booking_id).all()

        # Convert payments to list of dictionaries for response
        payments_data = [
            {
                'payment_id': payment.payment_id,
                'booking_id': payment.booking_id,
                'payment_date': payment.payment_date,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'status': payment.status
            } for payment in payments
        ]

        return jsonify(payments_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
