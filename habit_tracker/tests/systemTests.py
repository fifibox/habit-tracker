import unittest
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app.models import User
from app import create_app, db as _db

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

class TestHabitTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(10)  # Implicit wait for elements to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_title(self):
        self.driver.get("http://localhost:5000")  # Replace with your app's URL
        self.assertIn("Habit Tracker", self.driver.title)

    def test_login_page(self):
        self.driver.get("http://localhost:5000/login")  # Replace with your app's login URL
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.NAME, "submit")

        username_field.send_keys("testuser")
        password_field.send_keys("password")
        login_button.click()

        # Wait for the next page to load and check for a specific element
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        self.assertIn("Dashboard", self.driver.page_source)

