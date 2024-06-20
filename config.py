class Config:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/aldo"
    JWT_SECRET_KEY='safaris'
#class Config:
    # Database configuration
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/aldo_safaris"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking system
    
    # JWT configuration
    #JWT_SECRET_KEY = 'safaris'  # Make sure to use a secure key in production
    
    # Additional configurations (Optional but recommended)
    # DEBUG = True 