//este script es para hacer aparecer la posibles opciones de paises que tenemos.

//la función dentro se ejecutara cada vez que se escriba algo en el inpu, o que cambia la entrada:
$(document).on('input', 'input:text', function(evt) {
    //obtenemos lo que escribimos:
    var written = evt.target.value;


    var href = '/maps/search_country_ajax/';
    //console.log(href);

    $.ajax({
        url: href,//a donde se enviara la solicitud ajax.
        data: {
        'written': written//enviamos el id a la vista que corresponda.
        },
        success: function(response){//si hay exito en la respuesta entra aca.
        if(response.created){//si created es True entra aca, esto significa que se creo el like, o sea se dio like.
            //console.log(response.created);//se dio el like.
            //al elemento con id ('#svg_suitcase' + id) le cambiamos el atributo opacity, esto lo que hace es resatar el suitcase, indicando que le dimos like.
            //console.log(response.countries_list);

            //el resto del trabajo podriamos hacerlo en otra función:
            Add_Countries(response.countries_list);
        }
        else{//se quito el like.
            //al elemento con id ('#svg_suitcase' + id) le cambiamos el atributo opacity, haciendo invisible(NO TOTALMENTE) el suitcase, indicando que le SACAMOS EL LIKE.
            //console.log(response.created);
        }
        }
    })

});


function Add_Countries(msg) {
    //console.log("se recibio la llamada a esta función");
    //console.log(msg);
    //eliminamos los elementos option anteriores:
    const dad_element = document.getElementById("datalist_countries");
    //console.log(dad_element);
    dad_element.textContent = '';

    //ahora agregamos los nuevos elementos:
    for (let index = 0; index < msg.length; index++) {
        const CountryElement_option = document.createElement('option');
        CountryElement_option.setAttribute("value", msg[index]);
        CountryElement_option.classList.add('option_country');
        dad_element.appendChild(CountryElement_option);
    }
    
}
