document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');

    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(event.target);

            fetch('/signup', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                console.log('Signup Result:', result);

                if (result.success) {
                    window.location.href = '/userAccountPage.html';
                } else {
                    alert(`Signup failed: ${result.message}`);
                }
            })
            .catch(error => {
                console.error('Error during signup:', error);
                alert('Signup failed. Please try again.');
            });
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(event.target);

            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`Network response was not ok. Status: ${response.status}`);
                }
            })
            .then(result => {
                if (result.success) {
                    alert(`Login successful: ${result.message}`);
                    if (result.message === "Login successful") {
                        window.location.href = '/dashboard.html';
                    } else {
                        // Handle other success cases or show appropriate messages
                    }
                } else {
                    throw new Error('Empty response from the server.');
                }
            })
            .catch(error => {
                console.error('Error during login:', error);
                alert('Login failed. Please try again.');
            });
        });
    }
});