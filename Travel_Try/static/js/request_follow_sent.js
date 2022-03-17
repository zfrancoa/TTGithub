//script para cambiar en tiempo real el boton follow o Candel follow
$(".Follow").click(function (e) {//entramos cuando demos click en un elemento con clase Follow
    var href = $('.Follow').attr('href');//obtenemos el href de ese elemento(url enlazada con la vista que creo o elimina instancias de solicitud follow)
    var id = this.id;//obtenemos el id de ese elemento(id del usuario al que se le envia la solicitud)
    e.preventDefault();//previene que se redirija a href

        $.ajax({//solicitud ajax
            url: href,//donde se realizara la solicitud
            data: {//que datos enviaremos
                'id': id
            },
            success: function(response){//si hubo exito y recibimos una respuesta entra aca
                //console.log(response);//imprimimos en consola la respuesta obtenida
                if(response.created==false){
                    $('#Follow'+id).hide();
                }
            }
        })
    });