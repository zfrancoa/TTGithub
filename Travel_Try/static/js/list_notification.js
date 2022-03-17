//obtenemos el bloque de las solicitudes recibidas:
var container_block_received = document.getElementById("container_block_received");
        
//obtenemos el bloque de las solicitudes enviadas:
var container_block_sent = document.getElementById("container_block_sent");

// Cuando se de click en el contenedor, marcaremos el fondo de un color:
container_block_received.onclick = function() {
    container_block_received.style.backgroundColor = "rgb(231, 233, 235)";
}

// Cuando se de click en el contenedor, marcaremos el fondo de un color:
container_block_sent.onclick = function() {
    container_block_sent.style.backgroundColor = "rgb(231, 233, 235)";
}