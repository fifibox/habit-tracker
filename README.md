# Habit Tracker Web App

This is a Flask-based web application that helps users track their daily habits and visualize their progress over time. The app allows users to create custom habits, log habit completion daily, and visualize progress through interactive charts and annual grid views.  A key feature is the ability to share the yearly progress grid with friends, supporting motivation and accountability in a private, secure environment.

- **Design:**  
  - Clean, modern interface with responsive design.
  - Secure authentication, CSRF protection, and password reset via email.
  - Data privacy: all user data is private by default and only shared with explicit consent.
  - Visualizations (charts, grids) make progress easy to understand at a glance.
  - Modular codebase for easy maintenance and extension.

## Features

- 📝 Register and log in to your account securely
- ➕ Add and manage custom habits (e.g., early early, no alcohol)
- 📈 Log daily habit completion with a simple interface
- 📊 Visualize your progress with interactive graphs and annual grid charts
- 🤝 Share your yearly habit grid with other users in-app
- 👀 View shared grids from friends

## Tech Stack
- **UI Design:** Figma (https://www.figma.com/design/qop7xkCU1Lece0MVl2QWYZ/Habit-Tracker?node-id=1-394&p=f&t=qy4CecLQQ8tFjt0O-0)
- **Backend:** Python, Flask, Flask-Login, Flask-WTF
- **Frontend:** HTML, CSS, JavaScript, Charts.js
- **Database:** SQLite (via SQLAlchemy)
- **Interactivity:** AJAX, Fetch API
- **Email Integration:** Gmail API (for password reset)
- **Testing:** unittest, Selenium
- **Version Control:** Git + GitHub

## Viewing the application
https://habit-tracker-uelr.onrender.com
- test user: alice
- password: alice123

## Group contributions
This project was developed following agile methodology as a group assignment for Agile Web Development unit at the University of Western Australia.

How I contributed in this project: I created the Figma design and implemented dashboard stats view, weekly view and share function. 

The rest of the team members include Siqi Shen, Zaya Batnasan and Divyanshu Brijesh Singh. 

Original repo: https://github.com/erdenezaya/gc_2_app
