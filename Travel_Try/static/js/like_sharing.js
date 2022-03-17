//al dar click en el elemento con clase like_suitcase entramos a esta función.
//la clase like_suitcase la tienen los enlaces( <a> ) que nos dan la posibilidad de dar like.
$(".like_suitcase_sharing").click(function (e) {

    //console.log("sharing");
    var id_link = this.id;//obtenemos el id de este enlace este id es el id del sharing al que dimos like.
    var id_sharing=id_link.replace("sharing", "");//obtenemos solo el numero del id
    //console.log(id_link);
    //console.log(id);

    var href = $( this ).attr('href');//obtenemos el href de este elemento con clase like_suitcase.
    e.preventDefault();

    //Nos fijamos si contiene la clase que nos dira si ya habia like o no:
    var condition = $( this ).hasClass("there_is_not_like");

    //OBTENEMOS EL ID DEL SHARING:
    var svg=$(this).children("svg");
    //console.log(svg);
    var id_svg = svg.attr("id");
    //console.log(id_svg);
    var id_svg_remplace_1 = id_svg.replace("svg_suitcase", "");//al id obtenido le quitamos la cadena "svg_suitcase"
    var id = id_svg_remplace_1.replace(""+id_sharing, "");//a la cadena obtenida le quitamos la cadena del id del sharing, y obtemos el id del post

    //obtenemos el elemento(en un elemento de tipo <span>) con id="span_like{{post.id}}", ya que si o si tendremos que sumar o restar uno a este valor que contenga el elemento.
    var cant_string=$("#span_like"+id_sharing).html();
    //convertimos el valor a entero:
    var cant_int=parseInt(cant_string, 10);

    if (condition) {//clase: there_is_not_like

        //cambiamos clase a there_is_like:
        $( this ).removeClass("there_is_not_like");
        $( this ).addClass("there_is_like");

        //console.log(response.created);//se dio el like.
        //al elemento con id ('#svg_suitcase' + id) le cambiamos el atributo opacity, esto lo que hace es resatar el suitcase, indicando que le dimos like.
        // $('#svg_suitcase' + id_sharing + id ).css("opacity", "1")
        $('#path_sharing_heart_fill' + id_sharing + id).attr('fill','#ed4956')
        $('#path_sharing_heart_stroke'+ id_sharing + id).attr('stroke','#ed4956')




        //sumamos uno a la cantidad de likes
        var sum = cant_int+1;
        $("#span_like"+id_sharing).text(sum);

    } else {//clase: there_is_like
        //cambiamos clase a there_is_not_like:
        $( this ).removeClass("there_is_like");
        $( this ).addClass("there_is_not_like");

        //al elemento con id ('#svg_suitcase' + id) le cambiamos el atributo opacity, haciendo invisible(NO TOTALMENTE) el suitcase, indicando que le SACAMOS EL LIKE.
        // $('#svg_suitcase' + id_sharing + id).css("opacity", "0.3")
        $('#path_sharing_heart_fill' + id_sharing + id).attr('fill','white')
        $('#path_sharing_heart_stroke'+ id_sharing + id).attr('stroke','black')

        var sum = cant_int-1;
        $("#span_like"+id_sharing).text(sum);

    }

    //Usamos ajax solo si hay like:
    $.ajax({
        url: href,//a donde se enviara la solicitud ajax.
        data: {
        'id_post_like': id//enviamos el id a la vista que corresponda.
        },
        success: function(response){//si hay exito en la respuesta entra aca.
            if(response.created){//si created es True entra aca, esto significa que se creo el like, o sea se dio like.
                //console.log("se dio like")
            }
            else{//se quito el like.
                //console.log("se dio dislike")
            }
        }
    })
    
});