document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM Loaded');

    const lessonItems = document.querySelectorAll('.lesson-item');

    lessonItems.forEach(function (lessonItem) {
        lessonItem.addEventListener('click', function () {
            // Redirect to user account page on lesson item click
            window.location.href = '/userAccountPage.html'; // Replace with the correct URL
        });
    });

    const cartSection = document.getElementById('cart-section');
    const viewCartButton = document.getElementById('view-cart');

    if (cartSection && viewCartButton) {
        viewCartButton.addEventListener('click', function () {
            cartSection.style.display = (cartSection.style.display === 'none') ? 'block' : 'none';
        });
    } else {
        console.error('Cart section or view cart button not found.');
    }

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
                    window.location.href = '/user_account_page';
                } else {
                    if (result.message === 'Missing required fields') {
                        alert('Please fill in all required fields.');
                    } else {
                        alert(`Signup failed: ${result.message}`);
                    }
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
                if (!response.ok) {
                    throw new Error(`Network response was not ok. Status: ${response.status}`);
                }
                window.location.href = '/user_account_page';
            })
            .catch(error => {
                console.error('Error during login:', error);
                alert('Login failed. Please try again.');
            });
        });
    }
});