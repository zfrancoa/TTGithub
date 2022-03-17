from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from telegram.models import Chat_Message
from django.shortcuts import redirect
from users.models import FollowersRequest
from django.urls import reverse

# Create your views here.



###---COSAS LEGALES----####
@login_required
def about(request):


    #URL PARA RESETEAR EL TUTORIAL:
    url_reset_tutorial = reverse('reset_tutorial')


    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        

    return render(request, 'legals/about.html', {'received_follower_request': received_follower_request, 'url_reset_tutorial': url_reset_tutorial})



@login_required
def licenses(request):

 

    return render(request, 'legals/licenses.html', {'messages_unreaded':messages_unreaded.count()})



@login_required
def Terms_and_Conditions(request):


    return render(request, 'legals/Terms_and_conditions.html', {'messages_unreaded':messages_unreaded.count()})






@login_required
def Privacy_Policy(request):
    

    return render(request, 'legals/Privacy_policy.html', {'messages_unreaded':messages_unreaded.count()})

###--------------------###
# 


def Terms_and_Conditions_not_login(request):

    return render(request, 'legals/Terms_and_Conditions_not_login.html')


def Privacy_Policy_not_login(request):

    return render(request, 'legals/Privacy_Policy_not_login.html')


def urlmap(request):

    return render(request, 'legals/urlmap.html')




#vista para que el usuario pueda volver a ver los tutoriales
@login_required
def reset_tutorial(request):

    # Asignar un dato a la sesión
    request.session['view_tutorial'] = True    

    return redirect('home')