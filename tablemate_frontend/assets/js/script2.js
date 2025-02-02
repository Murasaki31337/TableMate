document.getElementById("registrationForm")?.addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Registration successful! Please log in.");
        window.location.href = "login.html";
    } else {
        alert(`Error: ${data.detail}`);
    }
});
document.getElementById("loginForm")?.addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "profile.html";
    } else {
        alert("Incorrect email or password.");
    }
});

async function displayProfile() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/protected/dashboard", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await response.json();

    if (response.ok) {
        document.getElementById("userName").textContent = data.message; // Modify based on response
    } else {
        alert("Session expired. Please login again.");
        logout();
    }
}

if (window.location.pathname.endsWith("profile.html")) {
    displayProfile();
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}


// Automatically load profile details if on profile page
if (window.location.pathname.endsWith("profile.html")) {
    displayProfile();
}

