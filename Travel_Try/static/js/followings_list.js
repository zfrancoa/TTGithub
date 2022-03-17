$(".FollowingDeleted").click(function (e) {//entramos cuando demos click en un elemento con clase Accept
    var FollowingDeleted_href = $('.FollowingDeleted').attr('href');//obtenemos el href de ese elemento
    var id_Following_Deleted = this.id;//obtenemos el id de ese elemento(id del usuario al que envio la solicitud)
    //console.log(id_Following_Deleted);
    e.preventDefault();//previene que se redirija a href

    $.ajax({//solicitud ajax
        url: FollowingDeleted_href,//donde se realizara la solicitud
        data: {//que datos enviaremos
            'id_Following_Deleted': id_Following_Deleted
        },
        success: function(response){//si hubo exito y recibimos una respuesta entra aca
            //console.log(response);//imprimimos en consola la respuesta obtenida
            if(response.Following_Deleted_ajax){
                //console.log(response.Following_Deleted_ajax);
                $('#MyFollowing'+id_Following_Deleted).hide();//Escondemos el elemento con id Accept+id
            }
        }
    })
});