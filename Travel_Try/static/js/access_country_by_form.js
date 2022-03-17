// Get the modal
var button_photo_country = document.getElementById("go_add");

button_photo_country.onclick = function() {
    //obtengo que option es:
    var input_element = document.getElementById("input_name_country");
    //console.log(input_element.value);

    //obtengo el id del elemento option:
    option_element_id = document.getElementsByClassName("option_element"+input_element.value)[0].id;
    
    //console.log(option_element_id);

    //obtenemos username del usuario logeado:
    var username = JSON.parse(document.getElementById('username').textContent);

    //redirijo:
    window.location.href = "/maps/GalleryView/"+option_element_id+'/'+username+'/';

}