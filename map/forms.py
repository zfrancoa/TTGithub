from django import forms

from map.models import WorldCountriesUser, WorldCountries
#Create your forms here:





#ModelFormes un tipo especial de formulario. Estos son formularios que se generan automáticamente a partir de un modelo. Puede incluir campos a través del atributo de campos .
class AddCountryForm(forms.ModelForm):#formulario a partir de un modelo existente
    class Meta:
        model = WorldCountriesUser
        fields = ['countries_user']
        #El resto de campos del modelo Comments no los incluimos en el formulario.
        #los incluiremos automaticament.
       
       #con widgets estamos agregando algunas cosas al campo comment, o sea cuando lo llamemos en un template ya tendra lo que le agregemos.
        widgets = {
            #el 'autocomplete': 'off' es para que el navegador no almacene las entradas antiguas en el input, y no aparesca el autocompletado.
            'countries_user': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'list': 'datalist_countries', 'id': 'write_country', 'placeholder' : 'Add country', 'name': 'searchcountry'}),
        }


    #en la vista que trata al formulario pasamos como argumento el usuario que llama al formulario, con el fin de usarlo en el metodo clean.
    #el metodo __init__ lo recibe y lo almacena en la variable user, la cual accedemos como self.user.
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['countries_user'].label = ""#quitamos la etiqueta del campo, o sea, no aparecera la etiqueta en el templates, por ejemplo en este caso, no aparecera :  Countries user*

    
    def clean_countries_user(self):#para ver si el pais existe y si aun no lo agregamos
        countries_user=self.cleaned_data.get('countries_user')

        exist_country = WorldCountries.objects.filter(countries_tot=countries_user)
        if exist_country:#ENTRA ACA SI EL PAIS EXISTE.
            country_add = WorldCountriesUser.objects.filter(countries_user__icontains=countries_user, username=self.user)#ACA OBTENEMOS SI ES QUE EXISTE, EL OBJETO QUE COINCIDA CON EL PAIS QUE SE ENVIO POR EL FORMULARIO Y CON EL ID DEL USUARIO LOGEADO.
            if country_add:#ENTRA ACA SI EL PAIS YA FUE ALGUNA VEZ AGREGADO POR EL USUARIO.
                raise forms.ValidationError('Error. The country has already been added previously')  
        else:
            raise forms.ValidationError('Error. This country does not exit')
        return countries_user
