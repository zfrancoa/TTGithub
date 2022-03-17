//al dar click en el elemento con clase like_suitcase entramos a esta función.
//la clase like_suitcase la tienen los enlaces( <a> ) que nos dan la posibilidad de dar like.
//$(".delete_comment_class").click(function (e) {
    $(document).on('click', '.delete_comment_class', function(e) {

        e.preventDefault();
    
        var id = this.id;//obtenemos el id de este enlace este id es el id del comentario a eliminar.
        //console.log(id);
    
        
        //eliminamos el bloque del comentario, lo eliminamos ahora y no dentro del ajax para que se remueva mas rapido, ya que la solicitud ajax podria tardar unos segundos en servidores de bajos recursos.
        $('#comment_container'+id).remove();
    
    
    
        //console.log(id);
        var href_comment = $( this ).attr('href');//obtenemos el href de este elemento con clase like_suitcase.
        //console.log(href_comment);
    
        
        $.ajax({
            url: href_comment,//a donde se enviara la solicitud ajax.
            data: {
            'id_comment': id//enviamos el id a la vista que corresponda.
            },
            success: function(response){//si hay exito en la respuesta entra aca.
                if(response.deleted){//si created es True entra aca, esto significa que se creo el like, o sea se dio like.
                    //console.log(response);
    
                   
                }
                else{
                    //console.log('NO ELIMINADO');
                    //si entra aca significa que el comentario no existe
                }
            },
            error: function (request, status, error) {
                //habilitamos el boton para que pueda volverse a enviar un comentario:
                //console.log('ERROR');
            }
        })
    });