from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change the database URI as needed
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
    db.create_all()
    print("Database tables created")

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/userAccountPage')
def user_account_page():
    return render_template('userAccountPage.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    home_address = request.form['homeAddress']
    city_town = request.form['cityTown']
    state = request.form['state']
    zip_code = request.form['zipCode']

    # Check if the username or email already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if existing_user or existing_email:
        response_data = {"success": False, "message": "Username or Email already exists. Please choose a different one."}
        return jsonify(response_data), 400

    new_user = User(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        home_address=home_address,
        city_town=city_town,
        state=state,
        zip_code=zip_code
    )

    db.session.add(new_user)
    db.session.commit()

    # Redirect the user to the login page after signup
    response_data = {"success": True, "message": "Signup successful"}
    return jsonify(response_data), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return "Invalid credentials. Please try again."

    # Here, you can store the logged-in user information in a session, or use any other authentication method.
    # For simplicity, let's just return a success message.
    return "Login successful!"

@app.route('/account')
def account():
    # Here, you need to implement user authentication logic.
    # For simplicity, let's assume the user is logged in and authenticated.
    # You can use session management or JWT tokens for a more secure implementation.

    # Fetch the user details from the database (replace 'current_username' with the authenticated user's username)
    current_username = 'example_username'
    user = User.query.filter_by(username=current_username).first()

    if not user:
        return "User not found."

    return render_template('accountPage.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)