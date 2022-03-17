$(document).ready(function() {
    $("#id_form_comment").submit(function(event) {

        event.preventDefault();

        //deshabilitamos el boton para que no se pueda enviar un comentario hasta que se haya imprimido el anterior:
        $('#input_button_comment').prop('disabled', true);


        //obtenemos algunas variables que nos ayudaran a armar el comentario:
        var url_delete_comment = JSON.parse(document.getElementById('url_delete_comment').textContent);

        var url_photo = JSON.parse(document.getElementById('url_photo').textContent);

        var user_name = JSON.parse(document.getElementById('user_name').textContent);
        
        var url_myprofile = JSON.parse(document.getElementById('url_myprofile').textContent);

        var username_post = JSON.parse(document.getElementById('username_post').textContent);
        
        var data_from_form = $(this).serializeArray()

        // console.log(data_from_form);
        // console.log(data_from_form[1]);
        // console.log(data_from_form[1].value);

        var content_comment = data_from_form[1].value;

        //////////////////CREAMOS EL COMENTARIO//////////////////////
        //creamos un div:
        const first_div = document.createElement('div');//creamos un elemento div.
        //le agregamos una clase al div, esta clase es para identificar el div al que luego en la respuesta AJAX le agregaremos un atribto id con el id del comentario:
        first_div.setAttribute("class", "add_id_div");

        
        //creamos un div:
        const second_div = document.createElement('div');//creamos un elemento div.
        //le agregamos una clase al div:
        second_div.setAttribute("class", "d-flex justify-content-between align-items-center mt-2");

        //creamos un div:
        const third_div = document.createElement('div');//creamos un elemento div.
        //le agregamos una clase al div:
        third_div.setAttribute("class", "d-flex flex-row align-items-center");

        //creamos un a:
        const first_a = document.createElement('a');//creamos un elemento a.
        //le agregamos otro atributo, href:
        first_a.setAttribute("href", ""+url_myprofile)            

        //creamos un img:
        const first_img = document.createElement('img');
        //agregamos algunos atributos:
        first_img.setAttribute("class", "rounded-circle mr-2");
        first_img.setAttribute("width", "30");
        first_img.setAttribute("height", "30");
        first_img.setAttribute("src", ""+url_photo);


        //creamos un span:
        const first_span = document.createElement('span');//creamos un elemento span.


        //creamos un small:
        const first_small = document.createElement('small');//creamos un elemento div.
        //agregamos algunos atributos:
        first_small.setAttribute("class", "font-weight-bold mr-1");

        //creamos un a:
        const second_a = document.createElement('a');//creamos un elemento a.
        //le agregamos una clase al div:
        second_a.classList.add('some-links');
        //le agregamos otro atributo, href:
        second_a.setAttribute("href", ""+url_myprofile)
        second_a.innerText = user_name;
                
        
        //creamos un small:
        const second_small = document.createElement('small');//creamos un elemento div.
        //agregamos algunos atributos:
        second_small.style.fontSize = "14px";                       
        //le agregamos contenido:
        second_small.innerText = content_comment; 

        //creamos un small:
        const third_small = document.createElement('small');//creamos un elemento div.
        
        //creamos un i:
        const first_i = document.createElement('i');//creamos un elemento div.
        //le agregamos una clase al div:
        first_i.setAttribute("class", "bi bi-trash");

        //creamos un a:
        const threth_a = document.createElement('a');//creamos un elemento div.
        //le agregamos una clase al a(element), esta clase es para identificar el a(element) al que luego en la respuesta AJAX le agregaremos un atribto id con el id del comentario:
        threth_a.setAttribute("class", "nav-link delete_comment_class add_id_a");
        //le agregamos otro atributo, href:
        threth_a.setAttribute("href", ""+url_delete_comment);
        //le agregamos otro atributo, href:
        //threth_a.setAttribute("id", "a");

        // //creamos un svg:
        var svg_delete_comment = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        //agregamos algunos atributos al svg:
        svg_delete_comment.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        svg_delete_comment.setAttribute("width", "16");
        svg_delete_comment.setAttribute("height", "16");
        svg_delete_comment.setAttribute("fill", "currentColor");
        svg_delete_comment.setAttribute("viewBox", "0 0 16 16");
        svg_delete_comment.setAttribute("class", "bi bi-trash");
        
        //creamos unos elementos path:
        var path1_delete = document.createElementNS("http://www.w3.org/2000/svg", "path");
        var path2_delete = document.createElementNS("http://www.w3.org/2000/svg", "path");
        //agregamos algunos atributos al path:
        path1_delete.setAttribute(
            'd',
            "M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
        );
        //agregamos algunos atributos al path:
        path2_delete.setAttribute(
            'd',
            "M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
        );
        //agregamos algunos atributos al path:
        path2_delete.setAttribute("fill-rule", "evenodd");

        //metemos los path dentro del svg:
        svg_delete_comment.appendChild(path1_delete);
        svg_delete_comment.appendChild(path2_delete);


        //creamos un div:
        const fouth_div = document.createElement('div');//creamos un elemento div.
        //le agregamos una clase al div:
        fouth_div.setAttribute("class", "d-flex align-items-center border-bottom");

        //creamos un div:
        const fifth_div = document.createElement('div');//creamos un elemento div.
        
        //creamos un small:
        const fourth_small = document.createElement('small');//creamos un elemento div.
        //agregamos algunos atributos:
        fourth_small.style.fontSize = "10px";                       
        //le agregamos contenido:
        //Agregamos el tiempo en que se hizo el comment: {{ detail.time_comment }}
        var today = new Date();  
        var date=today.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
        //CON LAS DOS LINEAS ANTERIORES CALCULAMOS LA HORA.
        fourth_small.innerText = date;    


        //COMENZAMOS A ARMAR LOS BLOQUES, LOS EMBOLSAREMOS UNO DENTRO DEL OTRO:
        fifth_div.appendChild(fourth_small);
        fouth_div.appendChild(fifth_div);

        threth_a.appendChild(svg_delete_comment);
        first_i.appendChild(threth_a);
        third_small.appendChild(first_i);


        first_small.appendChild(second_a);
        first_span.appendChild(first_small);
        first_span.appendChild(second_small);

        first_a.appendChild(first_img);


        third_div.appendChild(first_a);
        third_div.appendChild(first_span);


        second_div.appendChild(third_div);
        second_div.appendChild(third_small);


        first_div.appendChild(second_div);
        first_div.appendChild(fouth_div);

        //console.log(first_div);
        //////////////////CREAMOS EL COMENTARIO//////////////////////
        
        //Agregamos el comentario:
        $("#block_comment").prepend(first_div);
        
        
        //Creamos el comentario en la bbdd, con ayuda del ajax:
        $.ajax({ 
            data: $(this).serialize(), 
            type: $(this).attr('method'), 
            url: $(this).attr('action'), 
            success: function(response) {
                //console.log(response);

                //borramos el contenido de la barra donde se escribe el comentario:
                const CommentInputDom = document.querySelector('#input_comment_form');
                CommentInputDom.value = '';
                

                //AGREGAMOS LOS id A LOS ELEMENTOS CORRESPONDIENTES, ya que el comentario lo armamos afuera del ajax para que sea mas rapido, nos falta agregar los id correspondientes para que se pueda eliminar el comentario:
                //obtenemos el elemento que encierra todo el comentario, este elemento div debe estar identificado con el id del comentario asi luego puede eliminarse:
                const block_div_add_id = document.querySelector('div#block_comment div.add_id_div:first-child');
                //agregamos el id:
                block_div_add_id.setAttribute("id", "comment_container"+response.id);

                //obtenemos el elemento que del enlace que elimina el mensaje, este elemento a debe estar identificado con el id del comentario asi luego puede eliminarse:
                const block_a_add_id = document.querySelector('div#block_comment a.add_id_a:first-child');
                //console.log(block_a_add_id);
                //console.log('ananno');
                block_a_add_id.setAttribute("id", ""+response.id);
                //console.log(block_a_add_id);

                //habilitamos el boton para que pueda volverse a enviar un comentario:
                $('#input_button_comment').prop('disabled', false);
                

            },
            error: function (request, status, error) {
                //habilitamos el boton para que pueda volverse a enviar un comentario:
                $('#input_button_comment').prop('disabled', false);
            }

        });

    });

})
