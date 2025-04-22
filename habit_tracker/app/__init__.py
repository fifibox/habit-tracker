from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit_tracker.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    # app.config['SECRET_KEY'] = 'your_secret_key'  
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)  
    
    # Import your routes after app is initialized
    from app import routes

    return app