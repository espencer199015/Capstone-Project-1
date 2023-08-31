CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    homeaddress VARCHAR(100) NOT NULL,
    citytown VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zipcode INT NOT NULL
    -- Add other columns as needed
);

INSERT INTO users (username, password, email)
VALUES ('testuser', 'hashedpassword', 'test@example.com');