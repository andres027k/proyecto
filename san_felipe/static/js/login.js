document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    let errorMessage = document.getElementById("error-message");

    if (username === "" || password === "") {
        errorMessage.textContent = "Por favor, completa todos los campos.";
        return;
    }

    let response = await fetch("http://127.0.0.1:8000/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    let data = await response.json();

    if (response.ok) {
        alert("Inicio de sesión exitoso");
        window.location.href = "/pedido/";
    } else {
        errorMessage.textContent = data.error;
    }
});

const botonPedir = document.getElementById("botonPedir");

let pedido = [];

// Agregar productos al pedido
window.agregarAlPedido = function (nombre, precio) {
    pedido.push({ nombre, precio });
};

// Enviar pedido
if (botonPedir) {
    botonPedir.addEventListener("click", function () {
        if (pedido.length === 0) {
            alert("No has agregado productos al pedido");
            return;
        }
        
        // Guardar en localStorage
        localStorage.setItem("pedido", JSON.stringify(pedido));
        
        // Redirigir a la página de login o pedido
        window.location.href = "/login/";
    });
}

