//script para cambiar en tiempo real el boton follow o Candel follow
$(".botton_request").click(function (e) {//entramos cuando demos click en un elemento con clase Follow
    

    var href = $('.botton_request').attr('href');//obtenemos el href de ese elemento(url enlazada con la vista que creo o elimina instancias de solicitud follow)
    var id = this.id;//obtenemos el id de ese elemento(id del usuario al que se le envia la solicitud)
    // console.log(id);
    // console.log(href);

    e.preventDefault();//previene que se redirija a href

    var condition = $( this ).hasClass("follow_request");

    if (condition) {//clase: follow_request

        $('#'+id).html("Cancel");
        $('#'+id).removeClass('btn btn-primary follow_request');
        $('#'+id).addClass('btn btn-warning cancel_request');
        
    } else {//clase: cancel_request

        $('#'+id).html("Follow");
        $('#'+id).removeClass('btn btn-warning cancel_request');
        $('#'+id).addClass('btn btn-primary follow_request');
    }

    $.ajax({//solicitud ajax
        url: href,//donde se realizara la solicitud
        data: {//que datos enviaremos
            'id': id
        },
        success: function(response){//si hubo exito y recibimos una respuesta entra aca
            //console.log(response);//imprimimos en consola la respuesta obtenida

        }
    })
});
