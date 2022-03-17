from users.models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


from captcha.fields import CaptchaField


#Django viene con un formulario de registro de usuario integrado. Solo necesitamos configurarlo según nuestras necesidades, por lo tanto, si queremos el campo email debemos agregarlo nosotros.
#clase UserCreationForm: un ModelForm para crear un nuevo usuario.Tiene tres campos: username(del modelo de usuario) password1, y password2. Verifica eso, password1 y password 2coincide, valida la contraseña usando validate_password()y establece la contraseña del usuario usando set_password().
class NewUserForm(UserCreationForm):#FORMULARIO PARA REGISTRARSE
    
    email = forms.EmailField(required=True)
    captcha = CaptchaField()#agregamos el captcha
    accept_terms_and_conditions = forms.BooleanField()
    
    class Meta:
        #Con esto crearemos un formulario basándonos en los campos del modelo 
        #User, el cual contre los fields indicados.
        model = User#Tomamos como argumento el nombre del modelo y lo convierte en un Formulario Django.
        fields = ("username", "email", "password1", "password2", "captcha", "accept_terms_and_conditions")
        #El resto de campos del modelo User no los incluimos en el formulario.


    def clean_username(self):#para que no se repitan nombres de usuarios identicos, y que no distinga entre minusculas y mayusculas, esto es por ejemplo : si hay un usuairo llamado franco no permitara que exista uno llamado FRANCO, Franco, FrAnCo etc.
        username=self.cleaned_data.get('username')
        if len(username)>30:
            raise forms.ValidationError('EL nombre de usuario no puede contener mas de 30 caracteres.')
        #no hay problema en usar icontains porque el mismo formulario no nos deja enviarlo hasta no agregar algo al username, o sea no se puede dejar en blanco el username.
        #recordar que icontains no funciona con 'none', por lo tanto, si la variable 'username' esta vacia aparecera error. 
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError('El usuario ya esta registrado, pruebe con otro.')
        return username


    #El clean_<fieldname>()método se llama en una subclase de formulario, donde <fieldname>se reemplaza con el nombre del atributo de campo de formulario. Este método realiza cualquier limpieza que sea específica de ese atributo en particular, sin relación con el tipo de campo que es. A este método no se le pasa ningún parámetro. Deberá buscar el valor del campo en self.cleaned_datay recordar que será un objeto Python en este punto, no la cadena original enviada en el formulario (estará adentro cleaned_dataporque el clean()método de campo general , arriba, ya ha limpiado el datos una vez)
    def clean_email(self):#metodo para ver si el email ingresado al formulario ya existe
        email=self.cleaned_data.get('email')#se busca el campo email en el cleaned_data
        if User.objects.filter(email=email).exists():#aca nos fijamos si el email ingresado al formulario ya se encuenta en la BBDD, si fuera el caso, no deberia permitir registrar el usuario.
            raise forms.ValidationError('El email ya esta registrado, pruebe con otro.')
        #El valor de retorno de este método reemplaza el valor existente en cleaned_data, por lo que debe ser el valor del campo de cleaned_data(incluso si este método no lo cambió) o un nuevo valor limpiado.
        return email
    
    #Cada uno ModelForm también tiene un save() método. Este método crea y guarda un objeto de base de datos a partir de los datos vinculados al formulario.
    #Anule el save()método de un formulario modelo para cambiar los campos y atributos del modelo o llame a métodos personalizados antes de guardar en la base de datos.
    #Tenga en cuenta que si el formulario no ha sido validado , la llamada save()lo hará marcando form.errors. A se ValueErrorgenerará si los datos en el formulario no se validan, es decir, si se form.errorsevalúa como True.
    def save(self, commit=True):
        #save(commit=False):es útil cuando obtiene la mayoría de los datos de su modelo de un formulario, pero necesita completar algunos null=Falsecampos con datos que no son del formulario.Guardar con commit = False le da un objeto modelo, luego puede agregar sus datos adicionales y guardarlo.
        #super (nombre que deriva de "superclass") tiene la siguiente sintaxis general: super(subClase, instancia).método(argumentos)
        #Básicamente es un shortcut que permite acceder a la clase base de una clase derivada y delegar llamadas a métodos de esta, sin tener que conocer ni escribir el nombre de la clase base. Retorna un objeto proxy, que permite actuar como un camino de llamada a métodos de alguna clase padre, no retorna una referencia a la clase padre en si misma.
        #En este caso se usa para llamar al método save() de la clase padre UserCreationForm.
        user = super(NewUserForm, self).save(commit=False)
        #El metodo save se uso para poder incluir el campo de correo electrónico que agregamos a nuestro formulario de registro.
        user.email = self.cleaned_data['email']#se busca el campo email en el cleaned_data.
        if commit:#COMO ESTA EN TRUE ENTRA.
            user.save()#GUARDAMOS EL USUARIO, EL USERNAME, EL PASSWORD Y EL EMAIL, EL METODO SAVE SE NECESITO PARA PODER GUARDAR ESTE ULTIMO CAMPO(EMAIL).
        return user




#este formulario se usara para poder editar el username del usuario.
class UserForm(forms.ModelForm):#ACA ESTAMOS CREANDO UN FORMULARIO A PARTIR DE UN MODELO.
    #ModelForm es una clase que se utiliza para convertir directamente un modelo en un formulario Django.
    class Meta:
        model = User#Tomamos como argumento el nombre del modelo y lo convierte en un Formulario Django.
        fields = ('username',)
    
    def clean_username(self):#para que no se repitan nombres de usuarios identicos, y que no distinga entre minusculas y mayusculas, esto es por ejemplo : si hay un usuairo llamado franco no permitara que exista uno llamado FRANCO, Franco, FrAnCo etc.
        username=self.cleaned_data.get('username')
        #no hay problema en usar icontains porque el mismo formulario no nos deja enviarlo hasta no agregar algo al username, o sea no se puede dejar en blanco el username.
        #recordar que icontains no funciona con 'none', por lo tanto, si la variable 'username' esta vacia aparecera error. 
        #Usar User.objects.filter(username__icontains=username).exists() si hay problemas, y si no se quiere nombres de usuarios con mismos nombres que solo cambian en mayusculas y minusculas.
        #agregar el icontains no nos dejara crear un usuario llamado franco si por ejemplos existe uno llamado franco1.
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya esta registrado, pruebe con otro.')
        return username



#este formulario se usara para poder editar la photo y bio del usuario.
class ProfileForm(forms.ModelForm):#ACA ESTAMOS CREANDO UN FORMULARIO A PARTIR DE UN MODELO.
    #ModelForm es una clase que se utiliza para convertir directamente un modelo en un formulario Django.
    class Meta: 
        model = Profile#Tomamos como argumento el nombre del modelo y lo convierte en un Formulario Django.
        fields = ('bio','photo','private')

        #con widgets estamos agregando algunas cosas al campo comment, o sea cuando lo llamemos en un template ya tendra lo que le agregemos.
        widgets = {
            #el 'autocomplete': 'off' es para que el navegador no almacene las entradas antiguas en el input, y no aparesca el autocompletado.
            'bio': forms.TextInput(attrs={'id': 'textarea'}),
        }





class ChangeEmailForm(forms.ModelForm):#Formulario para cambiar email

    class Meta: 
        model=User#Tomamos como argumento el nombre del modelo y lo convierte en un Formulario Django.
        fields= ['email']
        

    #El clean_<fieldname>()método se llama en una subclase de formulario, donde <fieldname>se reemplaza con el nombre del atributo de campo de formulario. Este método realiza cualquier limpieza que sea específica de ese atributo en particular, sin relación con el tipo de campo que es. A este método no se le pasa ningún parámetro. Deberá buscar el valor del campo en self.cleaned_datay recordar que será un objeto Python en este punto, no la cadena original enviada en el formulario (estará adentro cleaned_dataporque el clean()método de campo general , arriba, ya ha limpiado el datos una vez)
    def clean_email(self):#metodo para ver si el email ingresado al formulario ya existe
        email=self.cleaned_data.get('email')#se busca el campo email en el cleaned_data
        if User.objects.filter(email=email).exists():#aca nos fijamos si el email ingresado al formulario ya se encuenta en la BBDD, si fuera el caso, no deberia permitir registrar el usuario.
            raise forms.ValidationError('El email ya esta registrado, pruebe con otro.')
        #El valor de retorno de este método reemplaza el valor existente en cleaned_data, por lo que debe ser el valor del campo de cleaned_data(incluso si este método no lo cambió) o un nuevo valor limpiado.
        return email