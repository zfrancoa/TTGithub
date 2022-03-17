//El evento onchange ocurre cuando el valor de un elemento ha cambiado.
ChangePhoto.onchange = evt => {
    const [file] = ChangePhoto.files
    if (file) {
        //El método estático URL.createObjectURL() crea un DOMString que contiene una URL que representa al objeto pasado como parámetro. 
        //sintaxis: objectURL = URL.createObjectURL(object);
        //object: Un objeto File o un objeto Blob para el que se creará la URL.
        image_profile.src = URL.createObjectURL(file)
    }
}

var btn_save = document.getElementById("save_profileform");//BOTON DE CONFIRMACION EN LA CABCERA DE LA PAGINA
var btn_save_notview = document.getElementById("buttonsaveform");//BOTON DEL FORM QUE NO VEMOS
// CUANDO SE HAGA CLICK EN EL SVG DE CONFIRMAR, SE HARA CLICK EN EL BOTON DEL FORMULARIO, PARA ENVIARLO:
btn_save.onclick = function() {
    btn_save_notview.click();
}
