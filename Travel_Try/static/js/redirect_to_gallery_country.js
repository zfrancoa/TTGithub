//al dar click en el elemento con clase like_suitcase entramos a esta función.
//la clase like_suitcase la tienen los enlaces( <a> ) que nos dan la posibilidad de dar like.
$(".desbordamiento").click(function (e) {

    var href_to_send_name_country = $( this ).attr('href');//obtenemos el href de este elemento con clase like_suitcase.
    e.preventDefault();//prevenimos el redireccionamiento
    //obtenemos contenido del enlace, sera "Tags: Country"
    contaminated_name_country = $( this ).text();
    //a lo obtenido le quitamos lo que no nos interesa, que es "Tags: "
    descontaminated_name_country = contaminated_name_country.replace("Tags: ", "");
    //console.log(contaminated_name_country);
    //console.log("name : " + descontaminated_name_country);
    
    //OBTENEMOS NOMBRE DE USUARIO DUEÑO DE LA PUBLICACION:
    var name_user_contaminated = $( this ).attr('class');
    name_user_descontaminated= name_user_contaminated.replace("text-primary desbordamiento ", "");
    
    // console.log(name_user_descontaminated);
    // console.log(name_user_contaminated);
        
    $.ajax({
        url: href_to_send_name_country,//a donde se enviara la solicitud ajax.
        data: {
            'name': descontaminated_name_country//enviamos el nombre a la vista que corresponda.
        },
        success: function(response){//si hay exito en la respuesta entra aca.
            if(response.Created){//si created es True entra aca, esto significa que se creo el like, o sea se dio like.
                window.location.href = "/maps/GalleryView"+'/'+response.country_found+'/'+name_user_descontaminated+'/';
                // console.log(window.location.host);
            }
            else{
                //si entra aca significa que el pais no existe.
                //console.log(response.Created);
            }
        }
    })  
    
});