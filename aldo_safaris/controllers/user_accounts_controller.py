from flask import Blueprint, request, jsonify
from datetime import datetime
from aldo_safaris.extensions import db, bcrypt,Bcrypt,JWTManager
from aldo_safaris.models.user_accounts import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

customer = Blueprint('auth', __name__, url_prefix='/api/v1/customer')
bcrypt=Bcrypt()
jwt=JWTManager()

@customer.route('/register', methods=['POST'])
def register():
    try:
        # Extract user data from request JSON
        data = request.json
        user_name = data.get('user_name')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')
       
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Basic input validation
        if not user_name or not email or not contact or not password:
            return jsonify({"error": "All fields are required"})

        if len(password) < 6:
            return jsonify({"error": "Your password must have at least 6 characters"})
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "This email is already registered"})
        if User.query.filter_by(contact=contact).first():
            return jsonify({"error": "This contact is already registered"})
        
        # Create a new user
        new_user = User(user_name=user_name, email=email, contact=contact,
                        password=hashed_password)
        
        # Add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer.route('/login', methods=["POST"])

def login():
    try:
        # Extract email and password from request JSON
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Retrieve user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Create access token and refresh token
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            # Return tokens in response
            return jsonify({'message': 'Login successful',
                            'access_token': access_token,
                            'refresh_token': refresh_token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        # Get the identity of the current user from the refresh token
        current_user_id = get_jwt_identity()

        # Create a new access token
        access_token = create_access_token(identity=current_user_id)

        return jsonify({'access_token': access_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer.route('/edit/<int:user_id>', methods=["PUT"])
@jwt_required()
def edit_user(user_id):
    try:
        # Check if the current user matches the user being edited
        current_user_id = get_jwt_identity()
        if current_user_id != str(user_id):
            return jsonify({'error': 'You are not authorized to perform this action'})

        # Extract user data from request JSON
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'})

        # Update user fields if provided in request
        # (Omitted for brevity)

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer.route('/delete/<int:user_id>', methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        # Check if the current user matches the user being deleted
        current_user_id = get_jwt_identity()
        if current_user_id != str(user_id):
            return jsonify({'error': 'You are not authorized to perform this action'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



    
        
    
    
    
    
    
    
    
    
    
    

    
    
    