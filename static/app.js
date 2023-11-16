document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM Loaded');
    const signupForm = document.getElementById('signup-form');
    console.log('Signup Form:', signupForm);
    const loginForm = document.getElementById('login-form');
    console.log('Login Form:', loginForm);

    // Assuming you have lesson items with a class 'lesson-item'
const lessonItems = document.querySelectorAll('.lesson-item');
const cartItemsList = document.getElementById('cart-items-list');

lessonItems.forEach(function (lessonItem) {
    lessonItem.addEventListener('click', function () {
        // Add the selected lesson to the cart
        const itemName = lessonItem.querySelector('h2').innerText;
        const listItem = document.createElement('li');
        listItem.innerText = itemName;
        cartItemsList.appendChild(listItem);
    });
});

     // View Cart Button Click Event
document.addEventListener('DOMContentLoaded', function () {
    const cartSection = document.getElementById('cart-section');
    const viewCartButton = document.getElementById('view-cart');

    if (cartSection && viewCartButton) {
        viewCartButton.addEventListener('click', function () {
            // Toggle the visibility of the cart section if cartSection exists
            cartSection.style.display = (cartSection.style.display === 'none') ? 'block' : 'none';
        });
    } else {
        console.error('Cart section or view cart button not found.');
    }
});

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
            console.log('Login Form Data:', Object.fromEntries(formData)); // Log form data

            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok. Status: ${response.status}`);
                }
                return response.json();
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