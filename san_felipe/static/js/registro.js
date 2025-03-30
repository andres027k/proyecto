document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let newUsername = document.getElementById("newUsername").value.trim();
    let email = document.getElementById("email").value.trim();
    let newPassword = document.getElementById("newPassword").value.trim();
    let registerMessage = document.getElementById("register-message");

    if (newUsername === "" || email === "" || newPassword === "") {
        registerMessage.textContent = "Por favor, completa todos los campos.";
        return;
    }

    let response = await fetch("http://127.0.0.1:8000/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: newUsername,
            email: email,
            password: newPassword
        })
    });

    let data = await response.json();

    if (response.ok) {
        alert("Registro exitoso. Ahora puedes iniciar sesión.");
        window.location.href = "/";
    } else {
        registerMessage.textContent = data.error;
    }
});


