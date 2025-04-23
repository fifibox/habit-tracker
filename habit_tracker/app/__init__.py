from flask import Flask
import os

# Initialize the Flask app
app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))

# You can configure your app here
# app.config['SECRET_KEY'] = 'your_secret_key'

# Import your routes after app is initialized
from app import routes

@app.route('/yearly')
def login():
    return render_template('yearly.html')