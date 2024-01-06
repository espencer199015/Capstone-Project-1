from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect
from flask import jsonify
import requests
import io
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://elizabetherlandson1:newpassword@localhost/capstoneproject1'
app.secret_key = 'abc123'
db = SQLAlchemy(app)

# Create the database table
def create_db():
        with app.app_context():
            db.create_all()
            print("Database tables created")
# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    home_address = db.Column(db.String(200), nullable=False)
    city_town = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    def is_active(self):
        return True 

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('homePage.html')

@app.route('/home')
def home_page():
    print(f"Session data: {session}")
    # Load user information if authenticated
    user = None
    if 'user_authenticated' in session and session['user_authenticated']:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            print(f"User authenticated: {user.username if user else 'None'}")
    return render_template('homePage.html', user=user)

@app.route('/lessonPage')
def lesson_page():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('lessonPage.html', user=user)

@app.route('/loginSignupPage')
def login_signup_page():
    return render_template('loginSignupPage.html')        

@app.route('/user_account_page')
@login_required
def user_account_page():
    user_id = session.get('user_id')
    print(session['cart'])
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('userAccountPage.html', user=user, session=session)
    
    # Handle cases where user or user_id is not found
    return render_template('error.html', message='User not found')

@app.route('/user_account_page_new')  # Renamed route to avoid duplication
@login_required
def user_account_page_new():
    return render_template('userAccountPage.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
# Validate that required fields are present in the form data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'home_address', 'city_town', 'state', 'zip_code']
        if not all(field in request.form for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
# Check if the email already exists in the database
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already exists. Please use a different email.'}), 409
        
        new_user = User(
            username=request.form['username'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            home_address=request.form['home_address'],
            city_town=request.form['city_town'],
            state=request.form['state'],
            zip_code=request.form['zip_code']
        )
        new_user.set_password(request.form['password'])  # Set hashed password

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['user_authenticated'] = True
        user_authenticated = True
        return jsonify({'success': True, 'message': 'Signup successful', 'user_authenticated': user_authenticated})

    except Exception as e:
        print(f"Error in signup route: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Verify hashed password
            login_user(user)
            
            # Store user information in the session upon successful login
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_authenticated'] = True  # Set user authentication status

            # Print session variables to check
            print(session)

            # Redirect to the user's account page upon successful login
            return redirect(url_for('user_account_page'))

        else:
            return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

# Example route for login success redirect
@app.route('/login_success_redirect')
def login_success_redirect():
    # Check if a redirect URL is stored in the session
    redirect_url = session.get('redirect_url', None)
    
    if redirect_url:
        # Redirect to the intended URL after successful login/signup
        return redirect(redirect_url)
    else:
        # If no redirect URL is stored, go to the home page
        return redirect(url_for('home'))

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        # Check if the user is authenticated
        if not session.get('user_authenticated'):
            return jsonify({'success': False, 'message': 'User not authenticated'}), 401

        # Get the user's account details
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Get the new username from the request JSON
        new_username = request.json.get('newUsername')

        # Update the user's username
        user.username = new_username
        db.session.commit()

        return jsonify({'success': True, 'message': 'User information updated successfully'})

    except Exception as e:
        print(f"An error occurred during user update: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during user update'}), 500

@app.route('/select_lesson', methods=['POST'])
def select_lesson():
    if not session.get('user_authenticated'):
        return redirect(url_for('login_signup_page'))  # Redirect non-authenticated users

    lesson_name = request.form['lesson_name']
    lesson_price = request.form['lesson_price']

    # Add the lesson to the user's session cart
    if 'cart' not in session:
        session['cart'] = []
    cart_list = session['cart']
    session['cart'] = cart_list
    session['cart'].append({'lesson_name': lesson_name, 'lesson_price': lesson_price})
    print(session['cart'])
    return redirect(url_for('user_account_page')) 

@app.route('/remove_lesson', methods=['POST'])
def remove_lesson():
    if not session.get('user_authenticated'):
        return redirect(url_for('login_signup_page'))  # Redirect non-authenticated users

    lesson_name = request.form['lesson_name']

    # Remove the lesson from the session cart
    if 'cart' in session:
        session['cart'] = [lesson for lesson in session['cart'] if lesson['lesson_name'] != lesson_name]

    return redirect(url_for('user_account_page'))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Log out the user
    # Clear session data related to user authentication
    session.pop('user_id', None)
    session['user_authenticated'] = False  # Reset user authentication status
    return redirect(url_for('home'))

# Change one of the select_lesson functions to select_lesson_remove
@app.route('/select_lesson_remove', methods=['POST'])
def select_lesson_remove():
    if not session.get('user_authenticated'):
        return redirect(url_for('login_signup_page'))  # Redirect non-authenticated users

    lesson_name = request.form['lesson_name']

    # Remove the lesson from the session cart
    if 'cart' in session:
        session['cart'] = [lesson for lesson in session['cart'] if lesson['lesson_name'] != lesson_name]

    return redirect(url_for('user_account_page'))

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    try:
        # Check if the user is authenticated
        if not session.get('user_authenticated'):
            return jsonify({'success': False, 'message': 'User not authenticated'}), 401

        # Get the user's account details
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Get the current date
        current_date = datetime.now().strftime("%m.%d.%Y")

        # Get lessons from the user's cart
        lessons_in_cart = session.get('cart', [])
        if not lessons_in_cart:
            return jsonify({'success': False, 'message': 'No lessons in the cart'}), 400

        # Prepare payload for the invoice
        payload = {
            "from": "Dream Ride Stables",
            "to": f"{user.first_name} {user.last_name}",
            "date": current_date,
            "items": []
        }

        # Add each lesson in the cart to the invoice payload
        for lesson in lessons_in_cart:
            item = {
                "name": lesson['lesson_name'],
                "quantity": 1,
                "unit_cost": float(lesson['lesson_price']),
                "description": f"Lesson details: {lesson['lesson_name']}"
            }
            payload["items"].append(item)

        # Make the request to the invoice generation API
        url = "https://invoice-generator.com"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        if response.ok:
            # Send the generated invoice as a file
            return send_file(
                io.BytesIO(response.content),
                as_attachment=True,
                download_name='invoice.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({'success': False, 'message': 'Invoice generation failed'}), 500

    except Exception as e:
        print(f"An error occurred during invoice generation: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during invoice generation'}), 500
    
create_db()

if __name__ == '__main__':
    app.run(debug=True)