// app.js
const express = require('express');
const app = express();

document.getElementById('signup-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);

  fetch('/signup', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json()) // Assuming your backend returns JSON
  .then(result => {
    if (result.success) {
      // Redirect the user to their user account page
      window.location.href = '/userAccountPage.html';
    } else {
      // Handle signup failure (e.g., display an error message)
      alert(result.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

document.getElementById('login-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);

  fetch('/login', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    alert(result); // Show the result returned from the backend
    if (result === "Invalid credentials. Please try again.") {
      // Handle error or display a message to the user
    } else {
      // Redirect the user to the dashboard or another page after successful login
      window.location.href = '/dashboard.html';
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

const { Client } = require('pg');

const client = new Client({
  user: 'your-username',
  host: 'localhost', // or your database host
  database: 'capstoneuseraccount',
  password: 'your-password',
  port: 5432 // default PostgreSQL port
});

client.connect();

app.get('/users', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM users');
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'An error occurred' });
  }
});

client.connect()
  .then(() => {
    console.log('Connected to the database');
  })
  .catch(error => {
    console.error('Error connecting to the database:', error);
  });

});
