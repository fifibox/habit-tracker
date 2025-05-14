import unittest
from flask import Flask, request
from flask_testing import TestCase


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/profile')
    def profile():
        return "Welcome to your profile", 200

    @app.route('/update_email', methods=['POST'])
    def update_email():
        email = request.form.get('email')
        if email:
            return "Email updated successfully", 200
        return "Invalid email", 400

    @app.route('/update_username', methods=['POST'])
    def update_username():
        username = request.form.get('username')
        if username:
            return "Username updated successfully", 200
        return "Invalid username", 400

    @app.route('/update_password', methods=['POST'])
    def update_password():
        password = request.form.get('password')
        if password:
            return "Password updated successfully", 200
        return "Invalid password", 400

    return app
