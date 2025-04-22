from flask import Flask, render_template
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/weekly')
def weekly():
    return render_template('weekly.html', active_page='weekly')

@app.route('/monthly')
def monthly():
    return render_template('monthly.html', active_page='monthly')

@app.route('/yearly')
def yearly():
    return render_template('yearly.html', active_page='yearly')