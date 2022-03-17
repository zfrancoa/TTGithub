
//Si la ventana gráfica tiene menos o igual a 700 píxeles de ancho, cambie el color de fondo a amarillo. Si es mayor a 700, cámbialo a rosa.

function mediaqueryfunction(x) {

    if (width_screen.matches) { // entramos aca solo si es menor a 750px
    
        //script para los touch-tactil events.

        //Configuramos los controladores de eventos:
        //Cuando se cargue la página, startup()se llamará a la función que se muestra a continuación:
        function startup() {
            //OBTENEMOS TODOS LOS path elements, pero no queremos a los path de ls iconos svg o sea no queremos los path que no pertenecen al mapa:
            var svg_map = document.querySelector('#svg_map');
            const paths = svg_map.querySelectorAll('path');
            //console.log(paths.length);
            //configuramos eventos de touch-tactil:
            paths.forEach(
                el => el.addEventListener("touchstart", handleStart, false)//El touchstart evento se activa cuando se colocan uno o más puntos de contacto en la superficie táctil.
            );
            paths.forEach(
                el => el.addEventListener("touchend", handleEnd, false)//El touchend evento se activa cuando uno o más puntos de contacto se eliminan de la superficie táctil.
            );
            paths.forEach(
                el => el.addEventListener("touchmove", handleMove, false)//El touchmove evento se activa cuando uno o más puntos de contacto se mueven a lo largo de la superficie táctil.
            );

            
            //Esto configura todos los detectores de eventos para nuestro <canvas>elemento para que podamos manejar los eventos táctiles a medida que ocurren.

            


        }

        //El DOMContentLoadedevento se activa cuando el documento HTML inicial se ha cargado y analizado por completo, sin esperar a que las hojas de estilo, las imágenes y los subcuadros terminen de cargarse.
        document.addEventListener("DOMContentLoaded", startup);//caudno se carge el elemento html inicial se ejecutara startup.

        //Seguimiento de nuevos toques.
        //Realizaremos un seguimiento de los toques en curso.
        var ongoingTouches = [];

        var IdsetTimeout = [];//areglo donde guardaremos todos los id de la funcion setTimeout, para luego, si se requiere, cancelarla.
        var Id_set;//variable para ir tomando los id de la funcion setTimeout.
        var status_touchmove=0;//variable para ver el estado de touchmove, o sea con esto vamos a ver si ya entramos al handleMove o no.

        //Cuando ocurre un evento touchstart, lo que indica que se ha producido un nuevo toque en la superficie, se llama a la función siguiente handleStart():
        function handleStart(evt) {
            //EN evt TENEMOS EL EVENTO OCURRIDO QUE RECIBIO ESTA FUNCION.
            evt.preventDefault();//Esto llama event.preventDefault()para evitar que el navegador continúe procesando el evento táctil (esto también evita que también se envíe un evento del mouse). 

            //changedTouches - una lista de los puntos de contacto cuyos elementos dependen del tipo de evento asociado:
            //Para el touchstart evento, que es este caso, es una lista de los puntos de contacto que se activaron con el evento actual.
            //los puntos de contactos son objetos Touch, estos objetos tienen propiedades basicas como por ejemplos :Touch.identifier, Touch.screenX, Touch.screenY, entre otras.
            var touches = evt.changedTouches;//obtenemos el contexto y sacamos la lista de puntos de contacto modificados de la propiedad del evento TouchEvent.changedTouches.



            for (var i = 0; i < touches.length; i++) {//recorremos los objetos touch y los iremos guardando en ongoingTouches arreglo.
                ongoingTouches.push(copyTouch(touches[i]));//el método push() añade uno o más elementos al final de un array y devuelve la nueva longitud del array.          
            }

            
            Id_set=setTimeout(function(){ cosillas(1); }, 400);//se ejecutara cosillas en 0.4s si antes no se cancela. 
            IdsetTimeout.push(Id_set);//almacenamos id de setTimeout por si luego debemos cancelarla.
            

        }

        function cosillas(params) {
            //para mostrar el text primero obtenemos el elemento text.
            var text_element = document.querySelector("#text");

            if (ongoingTouches.length < 2) {//nos fijamos si se dieron menos de 2 toques.
                //si se dio menos de dos toques marcamos el pais en azul y mostramos su nombre.
                //mostramos su nombre pero antes no fijamos si tiene la clase country_added.
                if (ongoingTouches[ongoingTouches.length-1].target.classList.contains('country_added')) {
                    var name = ongoingTouches[ongoingTouches.length-1].target.getAttribute('class');
                    name=name.replace('country_added', ''); 
                    text_element.textContent=name;//en el elemento text imprimimos name, nombre del pais.     
                }else{//si no contiene la clase country_added mostramos el nombre sin tratamiento.
                    text_element.textContent = ongoingTouches[ongoingTouches.length-1].target.getAttribute('class');//IMPRIMIMOS LA var name EN EL ELEMENTO CUYO ID SEA text.
                    ongoingTouches[ongoingTouches.length-1].target.classList.add('hover_effect');//marcamos el country en azul, agregando una clase. 
                }    
            
            } else {//cuanda haya mas de 2 toques.
                //nos fijamos si el toque anterior y el actual son sobre el mismo country.
                if (ongoingTouches[ongoingTouches.length-1].target.getAttribute('class') == ongoingTouches[ongoingTouches.length-2].target.getAttribute('class')) {
                    //accedemos al enlace
                    //pero solo accedemos si el pais contiene la clase country_added
                    if (ongoingTouches[ongoingTouches.length-1].target.classList.contains('country_added')) {
                        var link = ongoingTouches[ongoingTouches.length-1].target.parentElement.getAttribute("href");
                        
                        window.location.href=link;//FUNCIONA Y ES PURO JAVASCRIPT.
                    }

                } else {//que entre a este else significa que los toques no se hicieron sobre el mismo pais(path).
                    //hay que borrar el color del pais del ante ultimo toque, si el ultimo toque se dio en otro country(path).
                    //con este if nos fijamos si el elemento del ante ultimo toque contiene la clase hover_effect
                    if (ongoingTouches[ongoingTouches.length-2].target.classList.contains('hover_effect')) {
                        //le quitamos el color al pais del toque anterior, esto lo hacemos removiendo la clase que antes le agregamos.
                        ongoingTouches[ongoingTouches.length-2].target.classList.remove('hover_effect');
                    }
                    //mostramos nombre del nuevo pais, pero si contiene la clase country_added, se la quitamos:
                    if (ongoingTouches[ongoingTouches.length-1].target.classList.contains('country_added')) {
                        var name = ongoingTouches[ongoingTouches.length-1].target.getAttribute('class');
                        name=name.replace('country_added', '');  
                        text_element.textContent = name;//IMPRIMIMOS LA var name EN EL ELEMENTO CUYO ID SEA text.
                        
                    }else{//si el nombre del pais no contiene la clase country_added, mostramos el nombre sin tratamiento.

                        text_element.textContent = ongoingTouches[ongoingTouches.length-1].target.getAttribute('class');//IMPRIMIMOS en el elemento text.
                    }



                    //TAL VEZ, NO HAGA FALTA ESTE for.
                    //eliminaremos todos los toques, menos el ultimo que ´pertenece a nuevo pais, no lo eliminamos asi al dar otro toque podremos acceder al link
                    var large_touch=ongoingTouches.length;//si ponemos ongoingTouches.length directamente en el for habra problemas ya que el largo se va modificando en cada iteracion.;
                    for (var i = 0; i < large_touch-1; i++) {//recorremos todos los toques a eliminar, dejamos el ultimo, que supuestamente se dio en otro pais(path).
                        ongoingTouches.splice(0, 1);//se eliminan todos los toques si el anteriro y el actual no se dieron sobre el mismo country, se deja el ultimo toque para trabajar en el futuro.
                    }
                    //le agregamos la clase al nuevo pais.
                    if (ongoingTouches[ongoingTouches.length-1].target.classList.contains('hover_effect')==false) {
                        ongoingTouches[ongoingTouches.length-1].target.classList.add('hover_effect');
                    }
                    //hay que borrar todos los toques si el toque no se dio en un pais(path).
                }
            }
        }

        function handleMove(evt) {//FUNCION QUE SE EJECUTA CUANDO UN TOUCH SE MUEVE.
            //EN evt TENEMOS EL EVENTO OCURRIDO QUE RECIBIO ESTA FUNCION.
            evt.preventDefault();

            //A status_touchmove si la ponemos al final, aparecen errores.
            status_touchmove=1;//se entro al handleMove, entonces cambiamos el estado, que se usara en el futuro.

            //con este for borramos todos los setTimeout al enviarse un touchmove.
            for (let index = 0; index < IdsetTimeout.length; index++) {
                clearTimeout(IdsetTimeout[index]);          
            }

            //BORRAMOS EL NOMBRE DEL PAIS:
            var text_element = document.querySelector("#text");
            text_element.textContent = '';

            //estos 2 proximos if son por algunos problemas que aparecen, ya que se elimiann los toques pero no las clases.
            //removemos el color del ultimo pais tocado, si es que lo hubo.
            //removemos el color del ANTEultimo pais tocado, si es que lo hubo.
            if (ongoingTouches[ongoingTouches.length-1].target.classList.contains('hover_effect')) {
                ongoingTouches[ongoingTouches.length-1].target.classList.remove('hover_effect');
            }
            if (ongoingTouches[ongoingTouches.length-2].target.classList.contains('hover_effect')) {
                ongoingTouches[ongoingTouches.length-2].target.classList.remove('hover_effect');
            }
            //removemos el color del ANTEultimo pais tocado, si es que lo hubo.
            if (ongoingTouches[ongoingTouches.length-3].target.classList.contains('hover_effect')) {
                ongoingTouches[ongoingTouches.length-3].target.classList.remove('hover_effect');
            }




        }

        function handleEnd(evt) {//funcion que se ejecuta cuando un dedo se suelte d ela pantalla tactil.
            //EN evt TENEMOS EL EVENTO OCURRIDO QUE RECIBIO ESTA FUNCION.
            evt.preventDefault();
            //alert('toques que queda:'+ongoingTouches.length);


            if (status_touchmove == 1) {//aca esta la variable que antes cambiamos.
                //se eliminan todos los toques ya que despues de un move no tenemos que guardarlo, o sea podemos comenzar a guardarlos de nuevo.
                ongoingTouches=[];
                status_touchmove=0;
                //alert('no entra al facking if');
            }
            //alert('toques que queda:'+ongoingTouches.length);
            

        }

        //Copiar un objeto táctil:
        //Algunos navegadores (Safari móvil, por ejemplo) reutilizan objetos táctiles entre eventos, por lo que es mejor copiar las propiedades que le interesan, en lugar de hacer referencia a todo el objeto.
        function copyTouch({ identifier, pageX, pageY, target  }) {//de los objetos touch que pasamos, solo tomamos los atributos bascos que nos interesan y no todo el objeto. 
            return { identifier, pageX, pageY, target  };//retornamos estos 3 atributos.
        }

    } else {//suponemos que si entra aca estamos en una pc, y activamos los eventos de mouse
        
        var text_element_name = document.getElementById("text");

        //script para los mouse-events.
        //Configuramos los controladores de eventos:
        //Cuando se cargue la página, startup()se llamará a la función que se muestra a continuación:
        function startup() {
            var svg_map = document.querySelector('#svg_map');
            const paths = svg_map.querySelectorAll('path');
            //console.log(paths.length);
            //configuramos eventos de mouse:
            paths.forEach(
                el => el.addEventListener("mousemove", StarthoverEfecct)//El evento ocurre cuando el puntero se mueve mientras está sobre un elemento.
            );
            paths.forEach(
                el => el.addEventListener("mouseleave", FinishhoverEfecct)//El evento ocurre cuando el puntero se mueve fuera de un elemento.
            );
            paths.forEach(
                el => el.addEventListener("click", ClickonCountry)//El evento ocurre cuando el usuario hace clic en un elemento.
            );
            paths.forEach(
                el => el.addEventListener("dblclick", DoubleclickCountry)//El evento ocurre cuando el usuario hace clic en un elemento.
            );
            paths.forEach(
                el => el.addEventListener("mouseover", ShowName)
            );

        }

        //El DOMContentLoadedevento se activa cuando el documento HTML inicial se ha cargado y analizado por completo, sin esperar a que las hojas de estilo, las imágenes y los subcuadros terminen de cargarse.
        document.addEventListener("DOMContentLoaded", startup);//caudno se carge el elemento html inicial se ejecutara startup.

        var status_country=0;

        //funcion para mostrar nombre de pais
        function ShowName(event) {
            //obtenemos la clase del elemento path:
            var Name_Country = event.target.classList.value;

            //con este if limpiamos el valor obtenido:
            if(event.target.classList.contains('country_added') == true){
                var Name_Country = Name_Country.replace('country_added', '')
            }   

            //console.log(Name_Country);
            //imprimimos el nombre del pais en pantalla:
            text_element_name.innerHTML = Name_Country;


        }

        //Cuando el mouse entra en un country se ejecuta esta función:
        function StarthoverEfecct(event) {
            //nos fijamos si la clase hover_effect existe, y si no existe la agregamos con el fin que el pais se vea en celestito, que represente el efecto hover.
            if(event.target.classList.contains('hover_effect') == false){
                event.target.classList.add('hover_effect');
            }
        } 

        //Cuando el mouse sale de un country se ejecuta esta función:
        function FinishhoverEfecct(event) {
            //nos fijamos si el pais de donde salio el mouse tiene la clase hover_effect, si la tiene se la quitamos, asi sacamos el efecto hover.
            if(event.target.classList.contains('hover_effect')){
                event.target.classList.remove('hover_effect');
            }
        }

        //Cuando ocurre un click ejecutare esta función:
        function ClickonCountry(event) {
            //prevenimos que con un click se redireccione.
            event.preventDefault();//prevenimos la acción predeterminada que ocurre al hacer click en un enlace, esta acción es la redirección de la página.
        } 

        function DoubleclickCountry(event) {
            if(event.target.classList.contains('country_added')){//nos fiajmos si existe la clase country_added, sino no vale la pena ejecutar las lineas dentro del if.
                //La propiedad de sólo lectura de  Nodo.parentElement devuelve el nodo padre del DOM  Element, o null, si el nodo no tiene padre o si el padre no es un ElementDOM.
                //en este caso el padre de nuestro elemento siempre sera un enlace <a>.
                //getAttribute() devuelve el valor del atributo especificado en el elemento. Si el atributo especificado no existe, el valor retornado puede ser tanto null como ""
                //obtenemos el link del elemento padre que contiene el enlace.
                var link = event.target.parentElement.getAttribute("href");    
                window.location.href=link;//FUNCIONA Y ES PURO JAVASCRIPT.
            }
        }
                    
    }

}


var width_screen = window.matchMedia("(max-width: 750px)")
mediaqueryfunction(width_screen) // Call listener function at run time
width_screen.addListener(mediaqueryfunction) // Attach listener function on state changes

