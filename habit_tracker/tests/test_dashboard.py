import unittest
from flask import Flask, request

from flask_testing import TestCase

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/dashboard')
    def test_dashboard_is_loaded():
    # Simulate a request to the dashboard
        with app.test_client() as client:
            response = client.get('/dashboard')
            assert response.status_code == 200
            assert b"Welcome to your dashboard" in response.data
            
        return "Welcome to your dashboard", 200

    return app


