var url_reset_tutorial = JSON.parse(document.getElementById('url_reset_tutorial').textContent);


// Get the modal
var block_modal = document.getElementById("myblockmodal");

// Get the button that opens the modal
var Trigger = document.getElementById("Trigger");

//obtenemos el boton para aceptar restaurar los tutoriales:
var btn_accept = document.getElementById("accept_reset");

//obtenemos el boton para cancelar restaurar los tutoriales:
var btn_cancel = document.getElementById("cancel_reset");

// When the user clicks on the button, open the modal
Trigger.onclick = function() {
    //console.log('anano');
    block_modal.style.display = "block";
}

// When the user clicks on the button, open the modal
btn_accept.onclick = function() {
    window.location.href = url_reset_tutorial;
    block_modal.style.display = "none";
}

// When the user clicks on <span> (x), close the modal
btn_cancel.onclick = function() {
    block_modal.style.display = "none";
}