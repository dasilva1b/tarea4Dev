from django.http import HttpResponse
import datetime
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from isup.models import Pagina
from django.utils import simplejson
from random import randint

#View que despliega la pagina de inicio del sistema
def home(request):
  now=now = datetime.datetime.now()
  return render (request,'home.html',{'now':now})
  
def home2(request):
  x = request.POST['client_response']                                          
  response_dict = {} 
  y=Pagina.objects.order_by('-likes')
  
  #Metodo de seleccion: Se selecciona un numero del 1 al 10: Si dicho numero
  #esta en el rango [0..7] se escogera aleatoriamente una pagina de la mitad
  #de paginas mas votadas. De lo contrario se escoge la pagina de la mitad
  #menos votada.
  discriminante=randint(0,10)
  if (discriminante <=7):
    w=randint(0,len(y)//2)
    y=y[w].url
  else:
    w=randint((len(y)//2)+1,len(y)-1)
    y=y[w].url
  response_dict.update({'url': y })                                                                  
  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
  
def like(request):
  urlform=request.POST['iframeurl']
  updating=Pagina.objects.get(url=urlform)
  likes=updating.likes+1
  updating.likes=likes
  updating.save()
  return HttpResponse(status=204)
  
def dislike(request):
  urlform=request.POST['iframeurl']
  updating=Pagina.objects.get(url=urlform) #Si hago get debo garantizar que pagina este en bd
  if (updating.likes <> 0):
    likes=updating.likes-1
    updating.likes=likes
    updating.save()
  return HttpResponse(status=204)

