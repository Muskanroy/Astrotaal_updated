// frontend/static/js/script.js

document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = {
        // name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('pwd').value
    };

    fetch('http://127.0.0.1:8080/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Login successfully.') {
                sessionStorage.setItem('user_id', data.user_id);
                sessionStorage.setItem('session_id', data.session_id);
                console.log('Login successful, user_id and session_id stored in sessionStorage');
                // alert(data.message);
                console.log(data);
                console.log(sessionStorage.getItem('user_id'))
            }
            else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
