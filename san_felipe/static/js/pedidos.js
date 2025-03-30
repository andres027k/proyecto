document.addEventListener("DOMContentLoaded", function () {
    const botonCarrito = document.getElementById("verCarrito");
    const carrito = document.getElementById("carrito");

    botonCarrito.addEventListener("click", function () {
        carrito.classList.toggle("mostrar"); // Agrega o quita la clase "mostrar"
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Limpia el carrito al entrar en la página de pedido (si se desea).
    localStorage.removeItem('pedido'); // Esto limpia el carrito

    let pedido = JSON.parse(localStorage.getItem("pedido")) || [];

    function mostrarPedido() {
        let pedidoLista = document.getElementById("pedidoLista");
        let pedidoTotal = document.getElementById("pedidoTotal");
        let total = 0;

        pedidoLista.innerHTML = "";  // Limpiar la lista de productos

        // Iterar sobre los productos del pedido
        pedido.forEach(producto => {
            let item = document.createElement("li");
            item.innerText = `${producto.nombre} - $${producto.precio}`;
            pedidoLista.appendChild(item);
            total += producto.precio;
        });

        pedidoTotal.innerText = total;  // Mostrar el total
    }

    mostrarPedido();  // Llamar a la función para mostrar el pedido
});
