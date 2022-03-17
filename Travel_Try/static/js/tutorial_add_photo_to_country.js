function continue_tutorial(instance){
    var popup = document.getElementById("myPopup");


    if (typeof step === 'undefined') {
        //console.log('undefined');
        step = 0;
    }


    if (instance == 'go') {
        step = step+1;
        //console.log("step+1");
    }

    if (instance == 'return') {
        step = step-1;
        //console.log("step-1");
    }

    if (step < 0) {
        step = 0;
    }

    if (step > 4) {
        step = 5;
    }


    switch (step) {
        case 0:
            popup.innerHTML = 'Hi!, this is a tutorial to learn how to add a photo.';
            break;
        case 1:
            popup.innerHTML = 'To start, add a country, which you have visited. To do it, touch on inferior right corner.';
            break;
        case 2:
            popup.innerHTML = 'On the map, the added country will be highlighted by some color. To enter, follow the steps below.';
            break;
        case 3:
            popup.innerHTML = 'One option is to use the form at the top of the page, entering the country. For other option continue this tutorial.';
            break;
        case 4:
            popup.innerHTML = 'If you are on a computer, double click on the country, once inside, click on an image icon. If, on the other hand, you are on your cell phone, tap on the country, which should show you the name of the country at the bottom of the page, with this you will select the country, give it a second tap to access. The name of the country will display until you are redirected to the next page. Remember, not to move the map, otherwise you will have to select the country again. If you experience problems, you should update to the latest version of your browser.';
            break;
        default:
            popup.innerHTML = 'End.';
    }

    //console.log(step);

}

// When the user clicks on div, open the popup
function myFunction() {

    var popup = document.getElementById("popup_container");
    // toggle( String [, force] )
    //Cuando sólo hay un argumento presente: Alterna el valor de la clase; ej., si la clase existe la elimina y devuelve false, si no, la añade y devuelve true.
    //Cuando el segundo argumento está presente: Si el segundo argumento se evalúa como true, se añade la clase indicada, y si se evalúa como false, la elimina.

    popup.remove();

}



//Funcion para agregar una sesion que indique no queremos ver el tutorial:
$(".dont_view_tutorial").click(function (e) {

    var url_session = JSON.parse(document.getElementById('url_session').textContent);

    //Creamos el comentario en la bbdd, con ayuda del ajax:
    $.ajax({ 
        url: url_session, 
        success: function(response) {
            //console.log(response);
            //console.log("exito en ajax");
        },
        error: function (request, status, error) {
            //habilitamos el boton para que pueda volverse a enviar un comentario:
            //console.log("error en ajax");
        }

    });

});
