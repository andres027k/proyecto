document.addEventListener("DOMContentLoaded", function () { 
    const botonCarrito = document.getElementById("verCarrito");
    const carrito = document.getElementById("carrito");
    const cerrarCarrito = document.getElementById("cerrarCarrito");
    const listaCarrito = document.getElementById("listaCarrito");
    const cantidadCarrito = document.getElementById("cantidadCarrito");
    const totalCarrito = document.getElementById("total");
    const botonPedir = document.getElementById("botonPedir");
    const overlay = document.getElementById("overlay");

    // 🔄 Cargar el carrito desde localStorage (si hay datos guardados)
    let carritoCompras = JSON.parse(localStorage.getItem("pedido")) || [];

    // ✅ Mostrar / Ocultar carrito
    botonCarrito.addEventListener("click", function () {
        carrito.classList.toggle("mostrar");
        overlay.classList.toggle("mostrar");
        actualizarCarrito();
    });

    // ✅ Cerrar carrito
    cerrarCarrito.addEventListener("click", function () {
        carrito.classList.remove("mostrar");
        overlay.classList.remove("mostrar");
    });

    // ✅ Cerrar carrito si se hace clic fuera
    overlay.addEventListener("click", function () {
        carrito.classList.remove("mostrar");
        overlay.classList.remove("mostrar");
    });

    // ✅ Agregar productos al carrito con cantidad inicial de 1
    window.agregarAlCarrito = function (nombre, precio) {
        let productoExistente = carritoCompras.find(producto => producto.nombre === nombre);
        if (!productoExistente) {
            carritoCompras.push({ nombre, precio, cantidad: 1, seleccionado: true });
        } else {
            productoExistente.cantidad += 1; // Incrementar cantidad si ya existe
            productoExistente.seleccionado = true;
        }
        localStorage.setItem("pedido", JSON.stringify(carritoCompras));
        actualizarCarrito();
    };

    // ✅ Actualizar el carrito en la interfaz
    function actualizarCarrito() {
        listaCarrito.innerHTML = ""; // Limpiar la lista antes de actualizar
        let total = 0;
        let totalItems = 0;
        let productosValidos = carritoCompras.filter(producto => producto.seleccionado);

        if (productosValidos.length === 0) {
            listaCarrito.innerHTML = "<p>Tu carrito está vacío</p>";
            totalCarrito.textContent = "0";
            cantidadCarrito.textContent = "0";
            return;
        }

        productosValidos.forEach((producto, index) => {
            const subtotal = producto.precio * producto.cantidad;
            total += subtotal;
            totalItems += producto.cantidad;

            let item = document.createElement("li");
            item.innerHTML = `
                ${producto.nombre} - $${producto.precio.toLocaleString()} x 
                <span class="contador">
                    <button onclick="cambiarCantidad(${index}, -1)">-</button>
                    <span class="cantidad">${producto.cantidad}</span>
                    <button onclick="cambiarCantidad(${index}, 1)">+</button>
                </span>
                = $${subtotal.toLocaleString()}
                <button class="eliminar-producto" onclick="eliminarDelCarrito(${index})">❌</button>
            `;
            listaCarrito.appendChild(item);
        });

        totalCarrito.textContent = total.toLocaleString();
        cantidadCarrito.textContent = totalItems; // Mostrar la suma de cantidades

        // Guardar el carrito actualizado en localStorage
        localStorage.setItem("pedido", JSON.stringify(carritoCompras));
    }

    // ✅ Cambiar la cantidad de un producto en el carrito
    window.cambiarCantidad = function (index, cambio) {
        if (index >= 0 && index < carritoCompras.length) {
            carritoCompras[index].cantidad += cambio;
            if (carritoCompras[index].cantidad <= 0) {
                carritoCompras.splice(index, 1); // Eliminar si la cantidad es 0 o menor
            }
            actualizarCarrito();
            localStorage.setItem("pedido", JSON.stringify(carritoCompras));
        }
    };

    // ✅ Eliminar productos del carrito
    window.eliminarDelCarrito = function (index) {
        carritoCompras.splice(index, 1);
        localStorage.setItem("pedido", JSON.stringify(carritoCompras));
        actualizarCarrito();
    };

    // ✅ Verificar antes de redirigir a la página de pedido
    botonPedir.addEventListener("click", function () {
        let productosValidos = carritoCompras.filter(producto => producto.seleccionado);
        if (productosValidos.length === 0) {
            alert("⚠️ Tu carrito está vacío. Agrega productos antes de hacer un pedido.");
            return;
        }
        // Guardar el pedido en localStorage antes de redirigir
        localStorage.setItem("pedido", JSON.stringify(productosValidos));
        window.location.href = "/login/";
    });

    // 🛑 Cargar el carrito al abrir la página
    actualizarCarrito();
});

function mostrarCategoria(categoriaId) {
    // Ocultar todas las categorías
    document.querySelectorAll('.categoria').forEach(categoria => {
        categoria.classList.remove('activa');
    });

    // Mostrar la categoría seleccionada
    document.getElementById(categoriaId).classList.add('activa');
}
