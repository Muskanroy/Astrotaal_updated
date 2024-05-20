// frontend/static/js/script.js

document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('pwd').value
    };

    fetch('http://127.0.0.1:8080/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // alert(data.message);
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
