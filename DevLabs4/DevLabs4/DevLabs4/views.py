from django.http import HttpResponse
import datetime
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from isup.models import Pagina
from django.utils import simplejson
from random import randint
from twython import Twython, TwythonError

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
  
def twitter(request):
  #Creamos el objeto twython para interactuar con la API de twitter.
  APP_KEY='sa9BfxBBXo9dakoMLRdkw'
  APP_SECRET='N3RXxoBr6ryBRPE0XsS5Onsi66GBgsRl9j0zAarOyk'
  OAUTH_TOKEN='2283491449-a8Wp0dFP2Z1UXdMM42m3H9PZmiuO9ZqlQ8MI8kS'
  OAUTH_TOKEN_SECRET='ca3k5eNhUfoNdNctofVmjEviYTqiUz0Z1Nhx1r4UHgDAR'

  twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  
  #Diccionario que devolvera los tweets y sus links.
  response_dict = {} 
  #Parametro de la busqueda
  text=request.POST['client_response']
  text=text+" http"
  
  #Hago la busqueda y devuelvo un diccionario con la forma:
  #tweet1: text del tweet, link1: link del tweet, ...
  search_results = twitter.search(q=text, count=5)
  i=1
  tam=len(search_results['statuses'])
  if (tam == 5):
    for tweet in search_results['statuses']:
      key="tweet"+str(i)
      key2="link"+str(i)
      response_dict.update({key: tweet['text'] })   
      response_dict.update({key2: tweet['entities']['urls'][0]['url']}) 
      i=i+1
  else:
    response_dict.update({'tweet1': "null" })   
    response_dict.update({'link1': "null"}) 
    response_dict.update({'tweet2': "null" })   
    response_dict.update({'link2': "null"}) 
    response_dict.update({'tweet3': "null" })   
    response_dict.update({'link3': "null"}) 
    response_dict.update({'tweet4': "null" })   
    response_dict.update({'link4': "null"}) 
    response_dict.update({'tweet5': "null" })   
    response_dict.update({'link5': "null"}) 
    i=1
    for tweet in search_results['statuses']:
      key="tweet"+str(i)
      key2="link"+str(i)
      response_dict.update({key: tweet['text'] })   
      response_dict.update({key2: tweet['entities']['urls'][0]['url']}) 
      i=i+1
    
  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    
def opentwlink(request):
   response_dict = {} 
   link=request.POST['client_response']
   p= Pagina (url=link, likes=0) #Verificar que ya no este guardada
   p.save()
   response_dict.update({'url':link})
   return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
   

