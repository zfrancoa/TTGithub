from django import forms
from .models import Comments, report_post

#Create your forms here:







#ModelFormes un tipo especial de formulario. Estos son formularios que se generan automáticamente a partir de un modelo. Puede incluir campos a través del atributo de campos .
class CommentForm(forms.ModelForm):#formulario a partir de un modelo existente
    class Meta:
        model = Comments
        fields = ['comment']
        #El resto de campos del modelo Comments no los incluimos en el formulario.
        #los incluiremos automaticament.
       
       #con widgets estamos agregando algunas cosas al campo comment, o sea cuando lo llamemos en un template ya tendra lo que le agregemos.
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control', 'id': 'input_comment_form', 'placeholder' : 'Add a comment'}),
        }


#ModelFormes un tipo especial de formulario. Estos son formularios que se generan automáticamente a partir de un modelo. Puede incluir campos a través del atributo de campos .
class ReportPostForm(forms.ModelForm):#formulario a partir de un modelo existente
    class Meta:
        model = report_post
        fields = ['Why_reported']
        #El resto de campos del modelo report_post no los incluimos en el formulario.
        #los incluiremos automaticamente y otros en la vista.
       
       #con widgets estamos agregando algunas cosas al campo Why_report, o sea cuando lo llamemos en un template ya tendra lo que le agregemos.
        widgets = {
            'Why_reported': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Add a description'}),
        }

    