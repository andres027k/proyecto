document.addEventListener("DOMContentLoaded", function () {
    const carrusel = document.getElementById("carrusel");
    let platos = Array.from(document.querySelectorAll(".plato"));
    
    // Duplicamos los elementos para un efecto infinito
    platos.forEach(plato => {
        let clon = plato.cloneNode(true);
        carrusel.appendChild(clon);
    });

    const platoAncho = platos[0].offsetWidth + 15; // Ancho de cada tarjeta + margen
    let desplazamiento = 0;
    let velocidad = 1.5; // Velocidad de desplazamiento
    let intervalo;

    function moverCarrusel() {
        desplazamiento -= velocidad;
        carrusel.style.transform = `translateX(${desplazamiento}px)`;

        // Cuando se desplaza completamente un set de platos, reiniciamos
        if (Math.abs(desplazamiento) >= platoAncho * platos.length) {
            desplazamiento = 0; // Reinicia el desplazamiento
            carrusel.style.transition = "none"; // Evita parpadeos
        } else {
            carrusel.style.transition = "transform 0.2s linear";
        }
    }

    function iniciarAutoDesplazamiento() {
        intervalo = setInterval(moverCarrusel, 30);
    }

    function detenerAutoDesplazamiento() {
        clearInterval(intervalo);
    }

    iniciarAutoDesplazamiento();
    carrusel.addEventListener("mouseover", detenerAutoDesplazamiento);
    carrusel.addEventListener("mouseout", iniciarAutoDesplazamiento);

    // Botones de navegación manual
    document.querySelector(".carrusel-control.izquierda").addEventListener("click", function () {
        desplazamiento += platoAncho;
        carrusel.style.transform = `translateX(${desplazamiento}px)`;
    });

    document.querySelector(".carrusel-control.derecha").addEventListener("click", function () {
        desplazamiento -= platoAncho;
        carrusel.style.transform = `translateX(${desplazamiento}px)`;
    });
});

    // Manejo del formulario de reservas
    document.getElementById("reservaForm").addEventListener("submit", function(event) {
        event.preventDefault();
        let formData = new FormData(this);

        fetch("", { method: "POST", body: formData })
        .then(response => response.text())
        .then(() => {
            document.getElementById("mensaje").innerText = "Reserva enviada con éxito";
            this.reset();
        })
        .catch(() => {
            document.getElementById("mensaje").innerText = "Error al enviar la reserva";
        });
    });

    // Animaciones de iconos sociales
    document.querySelectorAll('.social-icon').forEach(icon => {
        icon.addEventListener('mouseover', () => icon.classList.add('animate'));
        icon.addEventListener('mouseout', () => icon.classList.remove('animate'));
    });
});


