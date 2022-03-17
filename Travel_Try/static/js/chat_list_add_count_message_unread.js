//ARREGLO CON LA CANTIDAD DE MENSAJES SIN LEER DE CADA USUARIO.
//este script agarra la cantidad de mensajes sin leer de cada usuarios y los agrega al html
var unread = JSON.parse(document.getElementById('array').textContent);
//console.log(unread);
//obtenemos todos los elementos donde debemos mostrar la cantidad de mensaje sin leer de cada uno.
var elementNodeReference = document.getElementsByClassName("block_message_introduce");
//obtenemos los enlaces con los link a los chat de los usuarios.

//console.log(link_users.length);
//console.log(elementNodeReference.length);
//console.log(unread.length);

if (elementNodeReference.length == unread.length) {
    //recorremos los elementos anteriores
    for (let index = 0; index < elementNodeReference.length; index++) {
        //creamos un enlace:
        const span = document.createElement('span'); 
        //agregamos una clase al enlace:
        span.classList.add('text-success');
        //tamaño de letra:
        span.style.fontSize = "12px";


        //le agregamos un texto:
        if (unread[index] < 1) {
            span.innerText ='there are not new messages' 
        }else if (unread[index] == 1) {
            span.innerText = unread[index]+' new message'
        }else{
            span.innerText = unread[index]+' new messages'
        }
        
        //metemos el enlace dentro del elemento que corresponde    
        elementNodeReference[index].appendChild(span);
    }


}





$(".background_block").click(function (e) {//entramos cuando demos click en un elemento con clase Accept
    $( this ).css('background-color', 'rgb(184, 207, 199)');
});


