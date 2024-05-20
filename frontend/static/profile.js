function updateProfile() {
    // Retrieve user_id from sessionStorage
    const userId = sessionStorage.getItem('user_id');
    const sessionId = sessionStorage.getItem('session_id');
    console.log('Retrieved user ID from sessionStorage:', userId);
    console.log('Retrieved session ID from sessionStorage:', sessionId);

    if (userId && sessionId) {
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            dob: document.getElementById('dob').value,
            time_of_birth: document.getElementById('time_of_birth').value,
            location_of_birth: document.getElementById('location_of_birth').value,
            phone_number: document.getElementById('phone_number').value,
            marital_status: document.getElementById('marital_status').value
        };

        fetch('http://127.0.0.1:8080/profile/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId, // Send session_id in headers
                'user-id': userId
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.log('User is not logged in.');
    }
}

document.getElementById('profile-form').addEventListener('submit', function (event) {
    event.preventDefault();
    updateProfile();
});