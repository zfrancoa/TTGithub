$(document).ready(function() {
            
    var FDeleted_id = '';

    var FDeleted_href = '';


    $(".Trigger").click(function (e) {//entramos cuando demos click en un elemento con clase Follow
       
        e.preventDefault();//previene que se redirija a href

        // Get the modal
        $("#myblockmodal").css("display", "block");

        //obtenemos id y href del usuario al cual eliminar de nuestros seguidores:
        FDeleted_href = $( this ).attr('href');
        FDeleted_id = this.id;
        FDeleted_id_origin = FDeleted_id.replace("del", "");
   
    });

    $("#accept_reset").click(function (e) {//entramos cuando demos click en un elemento con clase Follow
        
        
        //removemos el elemento bloque del usuario:
        $('#MyFollower'+FDeleted_id_origin).hide();//Escondemos el elemento con id Accept+id

        ajax:
        $.ajax({//solicitud ajax
            url: FDeleted_href,//donde se realizara la solicitud
            data: {//que datos enviaremos
                'FDeleted_id': FDeleted_id_origin
            },
            success: function(response){//si hubo exito y recibimos una respuesta entra aca
                //console.log(response);//imprimimos en consola la respuesta obtenida
            }
        })



        // Get the modal
        $('#myblockmodal').css("display", "none");
   
    });

    $("#cancel_reset").click(function (e) {//entramos cuando demos click en un elemento con clase Follow
    
        // Get the modal
        $('#myblockmodal').css("display", "none");

    });
})