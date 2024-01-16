# test_app.py
import os
import tempfile
import pytest
import sys

# Assuming 'app.py' is in the parent directory of 'tests'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify
from app import app, create_db, db, User



@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # Use SQLite for testing
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    client = app.test_client()

    with app.app_context():
        create_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_home(client):
    response = client.get('/')
    assert b'Home' in response.data

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'home_address': '123 Main St',
        'city_town': 'City',
        'state': 'State',
        'zip_code': '12345'
    })
    assert response.status_code == 409

def test_login(client):
    with client.session_transaction() as sess:
        sess['user_authenticated'] = True
        sess['user_id'] = 1
        sess['username'] = 'testuser'

    response = client.post('/login', data={'user_id': 1, 'username': 'testuser'})
    assert response.status_code == 302
    assert b'User Account Page' in response.data

def test_user_account_page(client):
    # Assuming you have a user with id=1 in your database
    user_id = 1

    # Log in the user
    response = client.post('/login', data={'user_id': user_id, 'username': 'testuser'})
    assert response.status_code == 200

    # Now make a request to the protected page
    response = client.get('/user_account_page', follow_redirects=True)
    assert response.status_code == 200
    assert b'User Account Page' in response.data

def test_select_lesson(client):
    with client.session_transaction() as sess:
        sess['user_authenticated'] = True
        sess['user_id'] = 1
    response = client.post('/select_lesson', data={
        'lesson_name': 'Test Lesson',
        'lesson_price': '19.99'
    })
    assert response.status_code == 302  # Redirect after selecting a lesson

# Add more tests for other routes and functionalities as needed