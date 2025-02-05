async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        document.getElementById('message').innerHTML = 'Please enter both email and password.';
        return;
    }

    const loginData = {
        email: email,
        password: password
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Change to application/json
            },
            body: JSON.stringify(loginData)  // Send JSON data
        });
        alert(loginData.password)  
        if (!response.ok) {
            throw new Error('Login failed. Invalid credentials.');
        }

        const data = await response.json();
        const token = data.access_token;

        document.getElementById('message').innerHTML = 'Login successful! Access token: ' + token;
        localStorage.setItem('access_token', token); // Save the token to localStorage
    } catch (error) {
        document.getElementById('message').innerHTML = 'Error: ' + error.message;
    }
}

async function register(event) {
    event.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
    });
    
    const data = await response.json();
    if (response.ok) {
        alert('Registration successful! You can now log in.');
        window.location.href = 'login.html';
    } else {
        alert('Registration failed: ' + data.detail);
    }
}

async function fetchProfile() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    
    const response = await fetch('http://localhost:8000/api/users/me', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    
    const data = await response.json();
    if (response.ok) {
        document.getElementById('profile-name').textContent = data.name;
        document.getElementById('profile-email').textContent = data.email;
    } else {
        alert('Failed to fetch profile');
        logout();
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.endsWith("profile.html")) {
        fetchProfile();
    }
});
