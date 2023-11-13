from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configure your PostgreSQL database settings here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://elizabetherlandson1:newpassword@localhost/capstoneproject1'

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
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

# Create the database table
def create_db():
    with app.app_context():
        db.create_all()
        print("Database tables created")

# Create the tables before running the app
create_db()

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
def user_account_page():
    return render_template('userAccountPage.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Validate that required fields are present in the form data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'home_address', 'city_town', 'state', 'zip_code']
        if not all(field in request.form for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        # Your signup code here
        # Assuming you have a user object created, for example:
        new_user = User(
            username=request.form['username'],
            password=request.form['password'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            home_address=request.form['home_address'],
            city_town=request.form['city_town'],
            state=request.form['state'],
            zip_code=request.form['zip_code']
        )
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # After successful signup, set user_authenticated to True
        user_authenticated = True
        return jsonify({'success': True, 'message': 'Signup successful', 'user_authenticated': user_authenticated, 'user': new_user})

    except Exception as e:
        print(f"Error in signup route: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

@app.route('/login', methods=['POST'])
def login():
    # Your login code here
    username = request.form['username']
    password = request.form['password']

    # Assuming you have a function to retrieve user details based on the login credentials
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        # After successful login, set user_authenticated to True
        user_authenticated = True
        return jsonify({'success': True, 'message': 'Login successful', 'user_authenticated': user_authenticated, 'user': user})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'}), 400

if __name__ == '__main__':
    app.run(debug=True)