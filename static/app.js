// app.js

document.getElementById('signup-form').addEventListener('submit', function (event) {
  event.preventDefault();
  
  const formData = new FormData(event.target);

  fetch('/signup', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    alert(result); // Show the result returned from the backend
    if (result === "Username or Email already exists. Please choose a different one.") {
      // Handle error or display a message to the user
    } else {
      // Redirect the user to the login page after successful signup
      window.location.href = '/loginSignupPage.html';
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
});
