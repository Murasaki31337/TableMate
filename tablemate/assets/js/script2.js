// Registration Functionality
document.getElementById("registrationForm")?.addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value; // User's full name
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const user = { username, email, password };
    localStorage.setItem("user_" + email, JSON.stringify(user));

    alert("Registration successful! Please log in.");
    window.location.href = "login.html";
});

// Login Functionality
document.getElementById("loginForm")?.addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const storedUser = JSON.parse(localStorage.getItem("user_" + email));

    if (storedUser && storedUser.password === password) {
        localStorage.setItem("loggedInUser", JSON.stringify({ username: storedUser.username, email: storedUser.email }));
        window.location.href = "profile.html";
    } else {
        alert("Incorrect email or password.");
    }
});

// Display Profile Information
function displayProfile() {
    const user = JSON.parse(localStorage.getItem("loggedInUser"));
    if (user) {
        document.getElementById("userName").textContent = user.username;
        document.getElementById("displayName").textContent = user.username; // Display user's full name
        document.getElementById("userEmail").textContent = user.email;
    } else {
        window.location.href = "login.html";
    }
}

// Logout Functionality
function logout() {
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
}

// Automatically load profile details if on profile page
if (window.location.pathname.endsWith("profile.html")) {
    displayProfile();
}
