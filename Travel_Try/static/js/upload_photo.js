//obtenemos el bloque con el link para agregar imagenes featured:
var container_add_featured = document.getElementById("container_add_featured");
        
// Get the button that opens the modal
var Trigger = document.getElementById("container_add_photo_country");


// Cuando se de click en el contenedor, marcaremos el fondo de un color:
Trigger.onclick = function() {
    Trigger.style.backgroundColor = "rgb(221, 223, 225)";
}

// Cuando se de click en el contenedor, marcaremos el fondo de un color:
container_add_featured.onclick = function() {
    container_add_featured.style.backgroundColor = "rgb(221, 223, 225)";
}

// Get the modal
var block_modal = document.getElementById("myblockmodal");


//obtenemos el boton para cancelar restaurar los tutoriales:
var btn_cancel = document.getElementById("close_button");

// When the user clicks on the button, open the modal
Trigger.onclick = function() {
    block_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
btn_cancel.onclick = function() {
    block_modal.style.display = "none";
}

//cuando el usuario hace click fuera del modal, lo quitamos:
window.onclick = function(event) {
    if (event.target == block_modal) {
        block_modal.style.display = "none";
    }
}




