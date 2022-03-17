//este script tomara del array los paises a los cuales se les debe cambiar la clase:


var countries = JSON.parse(document.getElementById('countries').textContent);
//console.log(countries);


for (let index = 0; index < countries.length; index++) {
    const element = countries[index];
    //console.log(element);

    //obtenemos los path correspondientes y le agregamos la clase como corresponde:
    elementList = document.getElementsByClassName(''+element);//OBTENEMOS TODOS LOS PATH QUR PERTENEZCAN AL PAIS.

    for (let index = 0; index < elementList.length; index++) {//RECORREMOS CADA PATH Y LE AGREGAMOS LA CLASE QUE CORRESPONDA.
        elementList[index].classList.add('country_added');

    }
}
