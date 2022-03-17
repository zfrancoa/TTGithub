from django.urls import path
from .views import about, licenses, Terms_and_Conditions, Privacy_Policy, Terms_and_Conditions_not_login, Privacy_Policy_not_login, urlmap, reset_tutorial



urlpatterns = [

    ###---COSAS LEGALES----####
    path('about/', about, name='about'),#Nos llevare a todo sobre lo legal.
    path('about/licenses', licenses, name='licenses'),#Nos llevare a todo sobre las licencias.
    path('about/TermsandConditions', Terms_and_Conditions, name='Terms_and_Conditions'),#Nos llevare a todo sobre terminos y condiciones.
    path('about/PrivacyPolicy', Privacy_Policy, name='Privacy_Policy'),#Nos llevare a todo sobre politicas de privacidad.
    path('about/Terms_and_Conditions_not_login', Terms_and_Conditions_not_login, name='Terms_and_Conditions_not_login'),#Nos llevare a todo sobre politicas de privacidad.
    path('about/Privacy_Policy_not_login', Privacy_Policy_not_login, name='Privacy_Policy_not_login'),#Nos llevare a todo sobre politicas de privacidad.
    path('about/urlmap', urlmap, name='urlmap'),#Nos llevare a todo sobre politicas de privacidad.
    path('reset_tutorial/', reset_tutorial, name='reset_tutorial'),#para resetear tutorial que ayud aa agregar foto a un pais


]
