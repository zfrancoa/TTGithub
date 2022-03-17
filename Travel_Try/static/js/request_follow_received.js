//este primer algoritmo es para cancelar o aceptar las solicitudes recibidas, ademas nos prepara las opciones de follow-unfollow-cancel, para ese usuario, dependiendo de si seguimos al usuario, o si le enviamos la solicitud o ninguna de las anteriores, de esto se encargara de manejarlo el segundo algoritmo.
$(document).on('click', '.first', function(e) { 
    e.preventDefault();//previene que se redirija a href
    // console.log('anano1');

    var href = $( this ).attr('href');//obtenemos el href de ese elemento(url enlazada con la vista que creo o elimina instancias de solicitud follow)
    
    var condition = $( this ).hasClass("accept");

    if (condition) {
        var id = this.id;//obtenemos el id 
        $('#'+id).removeClass('accept');
        $('#'+id).removeClass('first');
    } else {
        var id_rechazada = this.id;//obtenemos el id de ese elemento(id del usuario que envio la solicitud).
        var id = id_rechazada.replace('r','');//Remplazamos la r por nada, de esta manera obtenemos el id del usuario que corresponde.
        $('#'+id).removeClass('accept');
        $('#'+id).removeClass('first');
    }
    
    // console.log(id);
    // console.log(href);
    
    $('#block_cancel_request'+id).hide();

    

    var state = $( this ).hasClass("following");

    if (state) {
        $('#'+id).html("following");
        $('#'+id).removeClass('btn btn-primary following');
        $('#'+id).addClass('btn btn-warning botton_request unfollow');

        var url_delete_following = JSON.parse(document.getElementById('url_delete_following').textContent);
        $('#'+id).attr("href", url_delete_following);

    } else {

        var url_send = JSON.parse(document.getElementById('url_send').textContent);
        $('#'+id).attr("href", url_send);

        var state1 = $( this ).hasClass("follow");
        if (state1) {
            $('#'+id).html("Follow");
            $('#'+id).removeClass('btn btn-warning follow');
            $('#'+id).addClass('btn btn-primary botton_request follow_request');

        } else {
            $('#'+id).html("Cancel");
            $('#'+id).removeClass('btn btn-primary sent');
            $('#'+id).addClass('btn btn-warning botton_request cancel_request');
        }
    }

    // console.log($('#'+id).attr('class'));
    // console.log($('#'+id).attr('href'));

    $.ajax({//solicitud ajax
        url: href,//donde se realizara la solicitud
        data: {//que datos enviaremos
            'id': id
        },
        success: function(response){//si hubo exito y recibimos una respuesta entra aca

        }
    })


});



$(document).on('click', '.botton_request', function(e) { 
    // console.log('anano2');

    var href = $( this ).attr('href');//obtenemos el href de ese elemento(url enlazada con la vista que creo o elimina instancias de solicitud follow)
    var id = this.id;//obtenemos el id de ese elemento(id del usuario al que se le envia la solicitud)
    // console.log(id);
    // console.log(href);

    e.preventDefault();//previene que se redirija a href
    

    var condition = $( this ).hasClass("follow_request");

    if (condition) {//clase: follow_request

        $('#'+id).html("Cancel");
        $('#'+id).removeClass('btn btn-primary follow_request');
        $('#'+id).addClass('btn btn-warning cancel_request');
        
    } else {//clase: cancel_request or unfollow
        var condition_2 = $( this ).hasClass("unfollow");
        if (condition_2) {

            var url_send = JSON.parse(document.getElementById('url_send').textContent);
            $('#'+id).html("Follow");
            $('#'+id).removeClass('btn btn-warning unfollow');
            $('#'+id).addClass('btn btn-primary follow_request'); 
            
            $('#'+id).attr("href", url_send);

        } else {
            $('#'+id).html("Follow");
            $('#'+id).removeClass('btn btn-warning cancel_request');
            $('#'+id).addClass('btn btn-primary follow_request');  
        }
        
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
