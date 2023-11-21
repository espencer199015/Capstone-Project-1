from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from square.client import Client
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://elizabetherlandson1:newpassword@localhost/capstoneproject1'
db = SQLAlchemy(app)
access_token = "EAAAEJY2g4oGGzqP3J92OmmnFb8121A5E-XhpaxuNwb5SFdigzdDv574UA0OXvJY"
client = Client(access_token=access_token)

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
    return render_template('homePage.html')

@app.route('/lessonPage')
def lesson_page():
    return render_template('lessonPage.html')

@app.route('/loginSignupPage')
def login_signup_page():
    return render_template('loginSignupPage.html')        

@app.route('/user_account_page')
@login_required
def user_account_page():
    return render_template('userAccountPage.html')

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

        user_authenticated = True
        return jsonify({'success': True, 'message': 'Signup successful', 'user_authenticated': user_authenticated})

    except Exception as e:
        print(f"Error in signup route: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

# Modify the login route to verify hashed passwords
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Verify hashed password
            login_user(user)
            session['user_authenticated'] = True
            session['current_user'] = user
            return jsonify({'success': True, 'message': 'Login successful'})
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

@app.route('/select_lesson', methods=['POST'])
def select_lesson():
    if not session.get('user_authenticated'):
        return redirect(url_for('login_signup_page'))  # Redirect non-authenticated users

    lesson_name = request.form['lesson_name']
    lesson_price = request.form['lesson_price']

    # Add the lesson to the user's session cart
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'lesson_name': lesson_name, 'lesson_price': lesson_price})
    return jsonify({'success': True, 'message': 'Lesson added to cart'})

@app.route('/remove_lesson', methods=['POST'])
def remove_lesson():
    if not session.get('user_authenticated'):
        return redirect(url_for('login_signup_page'))  # Redirect non-authenticated users

    lesson_name = request.form['lesson_name']

    # Remove the lesson from the session cart
    if 'cart' in session:
        session['cart'] = [lesson for lesson in session['cart'] if lesson['lesson_name'] != lesson_name]

    return jsonify({'success': True, 'message': 'Lesson removed from cart'})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Log out the user
    # Clear session data
    session.pop('user_authenticated', None)
    session.pop('current_user', None)
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

    return jsonify({'success': True, 'message': 'Lesson removed from cart'})

@app.route('/get_payments', methods=['GET'])
def get_payments():
    try:
        # Retrieve payments
        result = client.payments.list_payments()

        if result.is_success():
            return jsonify({'success': True, 'payments': result.body})
        elif result.is_error():
            return jsonify({'success': False, 'error': result.errors}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

create_db()

if __name__ == '__main__':
    app.run(debug=True)