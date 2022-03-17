
//scripts para la creación y envio de mensajes, eliminación de mensjaes y estado de conexion o desconexión del usuario..
    
//message_unread: mensajes no leidos, lo pasaremos al otro usuario solo si esta conectado.
var messages_unread = JSON.parse(document.getElementById('array').textContent);
// console.log(messages_unread);
//console.log(messages_unread.length);




var message_received=0;//variable que usaremos de bandera para no generar un ciclo infinito de mensajes.


const chatLog = document.querySelector('#chat-log');//obtenemos el elemento con id 'chat-log', que es el div que encerrara a todos los mensaje

//A el dato resultante de arriba se accede de la siguiente manera:
//const value = JSON.parse(document.getElementById('hello-data').textContent);
//JSON.parse: el método  JSON.parse() analiza una cadena de texto como JSON, transformando opcionalmente el valor producido por el análisis.
//que devuelve JSON.parse: Retorna el objeto que se corresponde con el texto JSON entregado.
//.textContent devuelve la cadena que se obtiene del elemento con id "room_name".
const UserName = JSON.parse(document.getElementById('user-name').textContent);
//console.log(UserName);//NOMBRE DE USUARIO CON QUIEN ESTAMOS HABLANDO.

//El objeto WebSocket proporciona la API para la creación y administración de una conexión WebSocket a un servidor, así como también para enviar y recibir datos en la conexión.
//Para construir a WebSocket, usa el WebSocket()constructor.
//El constructor de WebSocket acepta un parámetro requerido y otro opcional:
//requerido: La URL a la cual se conecta, debe ser la URL con la cual el servidor WebSocket debe responder.
//WebSocket: Devuelve un WebSocket objeto recién creado.
//console.log('se crea el web socket apenas se entra a la pagina');
//console.log('SE CREO EL WEBSOCKET del resto');
// const chatSocket = new WebSocket(
//     //Es una buena práctica utilizar un prefijo de ruta común como /ws/para distinguir las conexiones WebSocket de las conexiones HTTP ordinarias porque facilitará la implementación de canales en un entorno de producción en determinadas configuraciones.
//     'ws://'
//     + window.location.host
//     + '/ws/chat/'
//     + UserName//NO SE CUAL HIRA, SI EL NOMBRE DEL USUARIO CON EL QUE HABLAMOS O EL NUESTRO.
//     + '/'
// );



// Correctly decide between ws:// and wss://
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
// {% if debug_mode %}
//var ws_path = ws_scheme + '://' + window.location.host + "/chat/" + UserName + "/"; // development
// {% else %}
var ws_path = ws_scheme + '://' + window.location.host + ":8001/chat/" + UserName + "/"; // production
// {% endif %}
var chatSocket = new WebSocket(ws_path);



//WebSocket.onmessage es una Propiedades del constructor.
//.onmessage: Un detector de eventos al que se llamará cuando se reciba un mensaje del servidor.
chatSocket.onmessage = function(e) {
    //e contiene el evento, o sea el mensaje recibido por el WebSocket.
    //JSON.parse: el método  JSON.parse() analiza una cadena de texto como JSON, transformando opcionalmente el valor producido por el análisis.
    //que devuelve JSON.parse: Retorna el objeto que se corresponde con el texto JSON entregado.
    //.data leemos los datos que contiene el evento, o sea el mensaje recibido.
    const data = JSON.parse(e.data);//en data tenenmos el texto.
    //.message: El message evento se activa cuando se reciben datos a través de un WebSocket.
    
    //Creo que aca nos deberiamos fijar si estamos en la interfaz del usuario que envio el mensaje, si estamos en su interfaz lo imprimimos, sino, no lo imprimimos.
    //En other_UserName tenemos el usuario con el que estamos hablando, lo mismo en UserName.
    //console.log('quien envia el mensaje: ' + data.other_UserName + ' = ' + UserName + ' de quien miramos la interfaz de mensajes');
    //en other_UserName tenemos el nombre de usuario de quien envia el mensaje.
    //UserName contiene el nombre de usuario con el que estemos chateando, o sea, del que estemos viendo la interfaz.
    //console.log(data.other_UserName);
    if (data.other_UserName == UserName) {//NOS FIJAMOS SI ESTAMOS EN LA INTERFAZ DE USUARIO CON QUIEN ESTAMOS HABLANDO
        if (data.action_consumer == 'delete_message'){//Si el mensaje recibido se debe a la eliminación de un mensaje en el chat.
            
            var son = document.getElementById("message"+data.id_message_delete);
            son.innerHTML= 'This message was deleted'

            
        }else if (data.action_consumer == 'my_message'){//Si el mensaje recibido se debe a la TX de un mensaje en el chat, pero para el caso de quien lo envio.
                
    

            //------//
            //agregamos el mensaje a la "fuerza"(o sea no nos fijamos si el otro usuario recibio el mensaje) en nuestra propia consola:


            //hay un problema con esto, y es que si el receptor no lo recibe, o sea, hubo un error, a nosotros nos aparecera el mensaje como que fue enviado, lo bueno es que no se guardara en la BBDD si no se recibe.
            const messageElement_div = document.createElement('div');//creamos un elemento div.
            messageElement_div.classList.add('message', 'sender');
            messageElement_div.setAttribute("id", 'message'+data.id_message);
            //console.log('message'+data.id_message);
            //console.log(messageElement_div);
            const messageElement_div3 = document.createElement('div');//creamos un elemento div.
            messageElement_div3.classList.add('delete_up_right');

            const element_a = document.createElement('a');//creamos un elemento a.
            element_a.classList.add('delete_messsage_link');
            element_a.setAttribute("href", "#");
            element_a.setAttribute("id", data.id_message);
            //console.log(element_a);
            
            var a_comp=document.getElementById('55');
            //console.log(a_comp);

            //obtenemos elelemento svg del delete
            var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            var path1 = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path1.setAttribute(
                'd',
                "M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"
            );
            svg.appendChild(path1);//path dentro de svg
            var path2 = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path2.setAttribute(
                'd',
                "M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1h7.08zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1h-7.08z"
            ); 
            svg.appendChild(path2);//path dentro de svg

            svg.setAttribute("width", "16");
            svg.setAttribute("height", "16");
            svg.setAttribute("fill", "currentColor");
            svg.setAttribute("viewBox", "0 0 16 16");
            svg.setAttribute("class", "bi bi-backspace");


            const messageElement_p = document.createElement('p');//creamos un elemento p.
            messageElement_p.innerText = data.message;//dentro del div creado metemos el mensaje recibido.

            const messageElement_div2 = document.createElement('div');//creamos un elemento div.
            messageElement_div2.classList.add('time_right');

            const messageElement_small = document.createElement('small');//creamos un elemento small.
            messageElement_small.setAttribute("id", "small"+data.id_message);
            //EN EL small VA LA HORA
            var today = new Date();  
            var date=today.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
            //CON LAS DOS LINEAS ANTERIORES CALCULAMOS LA HORA.
            messageElement_small.innerText = date;

            messageElement_div2.appendChild(messageElement_small);//agregamos el small dentro del div2.



            //El siguiente if es para ver si el otro usuario esta conectado, si lo esta, cada mensaje que enviamos le agregamos el visto, suponemos que el otro usuario vio nuestro mensaje por estar conectado.
            //Leemos el vlaor del elemento que nos indica el estado.
            var status_user = document.getElementById("status");

            if (status_user.innerHTML == "Connect") {//si el otro usuario esta conectado.
                //console.log('estado: '+status_user.innerHTML);
                //Creamos el elemento svg del "visto"
                
                var svg_read = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                var path1_read = document.createElementNS("http://www.w3.org/2000/svg", "path");
                path1_read.setAttribute(
                    'd',
                    "M8.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L2.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093L8.95 4.992a.252.252 0 0 1 .02-.022zm-.92 5.14.92.92a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 1 0-1.091-1.028L9.477 9.417l-.485-.486-.943 1.179z"
                );
                svg_read.appendChild(path1_read);//path dentro de svg

                svg_read.setAttribute("color", "green");
                svg_read.setAttribute("width", "16");
                svg_read.setAttribute("height", "16");
                svg_read.setAttribute("fill", "currentColor");
                svg_read.setAttribute("viewBox", "0 0 16 16");
                svg_read.setAttribute("class", "bi bi-check-all");

                //agregamos el svg dentro del div correspondiente
                messageElement_div2.appendChild(svg_read);//se mostrara como visto.

            }



            element_a.appendChild(svg);//agregamos el svg dentro del enlace.

            messageElement_div3.appendChild(element_a);//agreagamos el enlace a su div

            messageElement_div.appendChild(messageElement_div3);//agreagamoel div 3 dentro del div
            messageElement_div.appendChild(messageElement_p);//agreagamoel div 3 dentro del div
            messageElement_div.appendChild(messageElement_div2);//agreagamoel div 3 dentro del div
            

            chatLog.appendChild(messageElement_div);

            ScrollBottomInblock();//cada vez que agregamos un mensaje forzamos el scroll hacia abajo.
            //------//

        }else if (data.action_consumer == 'their_message'){//Si el mensaje recibido se debe a la TX de un mensaje en el chat, pero para el caso de quien lo recibio.
                
            //aca dentro imprimimos el mensaje.
            const messageElement_div = document.createElement('div');//creamos un elemento div.
            messageElement_div.classList.add('message', 'receiver');//en onmessage funcionsiempre se recibia mensajes, nunca seran nuestros.
            messageElement_div.setAttribute("id", 'message'+data.id_message);
            const messageElement_p = document.createElement('p');//creamos un elemento p.
            messageElement_p.innerText = data.message;//dentro del div creado metemos el mensaje recibido.
            const messageElement_div2 = document.createElement('div');//creamos un elemento div.
            messageElement_div2.classList.add('time_right');
            const messageElement_small = document.createElement('small');//creamos un elemento small.
            //EN EL small VA LA HORA
            var today = new Date();  
            var date=today.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
            //CON LAS DOS LINEAS ANTERIORES CALCULAMOS LA HORA.
            messageElement_small.innerText = date;

            messageElement_div2.appendChild(messageElement_small);//agregamos el small dentro del div2.
            messageElement_div.appendChild(messageElement_p);//agregamos el p dentro del div.
            messageElement_div.appendChild(messageElement_div2);//agregamos el div2 dentro del div.
            chatLog.appendChild(messageElement_div);

            ScrollBottomInblock();//cada vez que agregamos un mensaje forzamos el scroll hacia abajo.
        
            //Luego de imprimir en pantalla el mensaje recibido, enviamos de vuelta el id
        
        
        }else if (data.action_consumer == 'connect_user'){//manejamos mensajes debidos al estado de conecxión.
            
            if (data.status_user=='connected') {//si el mensaje recibido indica que el otro usuario se conecto
                //console.log('connected');
                if (message_received == 0) {//Este if es para evitar un ciclo sin fin de mensajes.
                    //console.log('entro');

                    //---------Cambiamos el contenido del div con id="status", para indicar que el usuario con quien hablamos esta conectado------------ //
                    var element_status=document.getElementById("status");
                    element_status.innerHTML = "Connect";
                    element_status.style.color = "green"; 
                    //---------Cambiamos el contenido del div con id="status", para indicar que el usuario con quien hablamos esta conectado------------ //

                    message_received=1;//indcamos que ya recibimos un mensaje, poniendo esta variable a 1 evitamos un ciclo de emnsajes sin fin.

                    //console.log(data.results);
                    //results puede contener IDs de mensajes no leidos
                    //esto suele pasar cuando usuario1 manda mensajes a usuario2, sin que usuario 2 este conectado, usuario1 se mantiene conectado, luego usuario2 se conecta, entonces, los mensajes que enviamos en este intervalo no apareceran como leidos, aunque el usuario2 este conectado, por ende, cuando usuario2 se conecta, por medio de consumer.py, mandamos los id de estos mensajes para marcarlos como leidos.
                    if (data.results != 'unnecessary') {//  unnecessary significa que ningun mensaje no leido hay que marcarlo como leido 
                        //console.log(data.results);
                        //desde el consumer enviamos los id de los mensajes no visto, ahora los cambiamos a visto:
                        for (let index = 0; index < data.results.length; index++) {
                            
                            //obtenemos el elemento donde ira el svg de "visto".
                            var small_element = document.getElementById('small'+data.results[index]);
                            //console.log(small_element);


                            //Creamos el svg, sino creamos un svg para cada mensaje entonces hay un problema, que solo se marca como leido el ultimo mensaje.
                            var svg_read = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                            var path1_read = document.createElementNS("http://www.w3.org/2000/svg", "path");
                            path1_read.setAttribute(
                                'd',
                                "M8.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L2.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093L8.95 4.992a.252.252 0 0 1 .02-.022zm-.92 5.14.92.92a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 1 0-1.091-1.028L9.477 9.417l-.485-.486-.943 1.179z"
                            );
                            svg_read.appendChild(path1_read);//path dentro de svg

                            svg_read.setAttribute("color", "green");
                            svg_read.setAttribute("width", "16");
                            svg_read.setAttribute("height", "16");
                            svg_read.setAttribute("fill", "currentColor");
                            svg_read.setAttribute("viewBox", "0 0 16 16");
                            svg_read.setAttribute("class", "bi bi-check-all");
                            //Hasta ahora fue creado el svg.
                            //console.log("a punto de poner el visto")
                            small_element.appendChild(svg_read);
    
                        }
                    }
                    //console.log("se envio mensaje desde js a consumer");

                    //enviamos un mensaje al otro usuario para indicar que recibimos su mensaje de que se encuentra conectado.
                    //o sea, sabra que sabemos que esta conectado, por ende tambien estamos conectados, entonces, el otro usuario nos marcara como conectado.
                    chatSocket.send(JSON.stringify({
                        'action':'connect'//esta variable sera leida en el consumidor para saber de que trata el mensaje enviado, en este caso se trata de eliminar un mensaje.
                    }));

                }

            }else if (data.status_user=='disconnect') {//si el mensaje recibido indica que el otro usuario se desconecto

                //Cambiamos el contenido del div con id="status" a desconectado
                var status_element=document.getElementById("status");
                status_element.innerHTML = "Disconnect";
                status_element.style.color = "red";
                message_received=0;//para que si se vuelva a conectar se pueda cambiar el estado a connect.
            }
        
            
            
        }
    
    }
    
};









//WebSocket.onclose: Es Un detector de eventos al que se llamará cuando se cierre la conexión.
//La WebSocket.onclosepropiedad es un  controlador de eventos que se llama cuando la conexión de WebSocket readyStatecambia a  CLOSED.
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');//imprimimos un mensaje de error en la consola web.
};


//con esto mantenemos fiajdo el input donde escribimos el mensaje, o sea luego de escribir un mensaje y enviarlo, no debemos dar click nuevamente en el input, ya estara fijado.
//FocusInput();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    //console.log("NO SE DEBE ENTRAR ACA AL ELIMINAR UN MENSAJE");
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

//cuando se de click en el elemento con id "chat-message-submit" se ejecutara la funcion de abajo, o sea, cuando se de click para enviar un mensaje.
document.querySelector('#chat-message-submit').onclick = function(e) {
    //console.log("NO SE DEBE ENTRAR ACA AL ELIMINAR UN MENSAJE");
    //con las siguientes dos lineas obtenemos el mensaje que se envio.
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;



    //El siguiente if es para ver si el otro usuario esta conectado, si lo esta, cada mensaje que enviamos le agregamos el visto, suponemos que el otro usuario vio nuestro mensaje por estar conectado.
    //Leemos el vlaor del elemento que nos indica el estado.
    var state_other_user = document.getElementById("status").innerHTML;
    //CON ESTE VALOR INDICAREMOS SI ACTUALIZAMOS LA BBDD Y MARCAMOS COMO LEIDO EL MENSAJE.
    

    //Recordar que en chatSocket tenmos el objeto WebSocket.
    //.send es un metodo de los WebSocket.
    //WebSocket.send(data): Pone en cola los datos que se van a transmitir.
    //El método JSON.stringify() convierte un objeto o valor de JavaScript en una cadena de texto JSON.
    //CON WebSocket.send(data) ENVIAMOS data AL SERVIDOR.
    if (message) {//nos fijamos si la variable message contiene algun valor, si no contiene nada, no enviamos ningun mensaje.
        //console.log("EL MENSAJE FUE ENVIADO AL WEBSOCKET");
        chatSocket.send(JSON.stringify({
            'action':'message',//esta variable sera leida en el consumidor para saber de que trata el mensaje enviado, en este caso se trata de que se envio un mensaje en el chat.
            'message': message,
            'state_other_user':state_other_user
        }));
    }

    messageInputDom.value = '';//una vez enviado el mensaje, ponemos en blanco la entrada donde se escriben los mensajes. 
    FocusInput();

};



//función para eliminar de a un mensaje:
$(document).on('click', 'a.delete_messsage_link', function(e) {
    e.preventDefault();//prevenimos redirrecion al link
    var id = this.id;//obtenemos el id de este enlace este id es el id del post al que damos like.
    var href = $('.delete_messsage_link').attr('href');//obtenemos el href de este elemento con clase like_suitcase.
    
    //console.log(id);
    //console.log(href);
    //console.log("SE ELIMINARA UN MENSAJE, JS -->CONSUMER");

    if (id) {//nos fijamos si la variable id contiene algun valor, si no contiene nada, no enviamos ningun mensaje.
        //console.log("EL MENSAJE FUE ENVIADO AL WEBSOCKET");
        chatSocket.send(JSON.stringify({
            'action':'delete',//esta variable sera leida en el consumidor para saber de que trata el mensaje enviado, en este caso se trata de eliminar un mensaje.
            'id_message_delete': id//id del mensaje a eliminar
        }));
    }
    //eliminamos mensaje de nuestro chat.

    var son = document.getElementById("message"+id);
    son.innerHTML= 'This menssage was deleted'
    
});


//funcion que utilizaremos para fijar el elemento input donde escribimos los mensajes
//o sea al enviar un mensaje todavia podremos seguir escribiendo sin tener que tocar en el elemento 'input' nuevamente.
function FocusInput(){
    document.querySelector('#chat-message-input').focus();
}


// Forzar el Scroll abajo del todo
function ScrollBottomInblock(){
    var block = document.getElementById("chat_main");
    block.scrollTop = block.scrollHeight;
}
//console.log('anda pa bajo');    
ScrollBottomInblock();
