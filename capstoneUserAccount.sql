CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    home_address VARCHAR(200) NOT NULL,
    city_town VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10) NOT NULL
);

INSERT INTO users (username, password, first_name, last_name, email, home_address, city_town, state, zip_code)
VALUES ('testuser', 'hashedpassword', 'John', 'Doe', 'test@example.com', '123 Main St', 'Anytown', 'Some State', '12345');