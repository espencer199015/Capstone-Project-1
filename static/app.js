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
    
    // Check if the edit button element is found
    const editBtn = document.getElementById('edit-btn');
    if (editBtn) {
        editBtn.addEventListener('click', function () {
            console.log('Edit button clicked');

            // Toggle visibility of edit form
            const editForm = document.getElementById('edit-form');
            if (editForm) {
                editForm.style.display = (editForm.style.display === 'none') ? 'block' : 'none';
                console.log('Edit form visibility toggled:', editForm.style.display);
            } else {
                console.error('Edit form not found');
            }
        });
    } else {
        console.error('Edit button not found');
    }
    // Define an empty checkout function
    function checkout() {
        // You can implement the logic for the checkout process here
        console.log("Checkout button clicked");
    }

    // Add an event listener for the form submission
    const editUserForm = document.getElementById('edit-user-form');
    if (editUserForm) {
        editUserForm.addEventListener('submit', function (event) {
            event.preventDefault();
            console.log('Form submitted. Implement the logic to update user information.');
            // Implement the logic to update user information
            // Get the new username from the form
            const newUsername = document.getElementById('new-username').value;
            const newPassword = document.getElementById('new-password').value;
            const newEmail = document.getElementById('new-email').value;
            const newFirstName = document.getElementById('new-first-name').value;
            const newLastName = document.getElementById('new-last-name').value;
            const newHomeAddress = document.getElementById('new-home-address').value;
            const newCityTown = document.getElementById('new-city-town').value;
            const newState = document.getElementById('new-state').value;
            const newZipCode = document.getElementById('new-zip-code').value;

            // Implement the logic to update user information
            fetch('/update_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    newUsername: newUsername,
                    newPassword: newPassword,
                    newEmail: newEmail,
                    newFirstName: newFirstName,
                    newLastName: newLastName,
                    newHomeAddress: newHomeAddress,
                    newCityTown: newCityTown,
                    newState: newState,
                    newZipCode: newZipCode,
                    // Add other form fields as needed
                }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    // Log the response for debugging
                    console.log('Update User Response:', response);
                    // Handle a successful response (e.g., display a success message)
                    console.log('User information updated successfully');
                    // Reload the user account page to reflect the changes
                    location.reload();
                })
                .catch(error => {
                    // Handle errors if the request fails
                    console.error('Error updating user information:', error);
                    // Optionally, display an error message to the user
                });
        });
    }

    function viewCart() {
        // Add any logic needed when clicking the "View Cart" button
        // For example, you might open a modal or navigate to a cart page
        console.log("View Cart button clicked");
    }
if (document.getElementById('checkout-btn')){
    document.getElementById('checkout-btn').addEventListener('click', function () {
        fetch('/generate_invoice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // Add any necessary payload data for invoice generation here
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob();
            })
            .then(blob => {
                // Create a temporary link element
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = 'document.pdf';
                // Append the link to the body
                document.body.appendChild(link);
                // Trigger a click on the link to start the download
                link.click();
                // Remove the link from the document
                document.body.removeChild(link);
            })
            .catch(error => {
                // Handle errors if the request fails
                console.error('Error:', error);
                // Optionally, display an error message to the user
            });
    });
}
});