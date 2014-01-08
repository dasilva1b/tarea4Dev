from django.db import models

# Create your models here.
#Cada objeto pagina tiene el url del website al cual hace referencia
#y los likes que se le han dado.
class Pagina(models.Model):
    url = models.CharField(max_length=130)
    likes = models.IntegerField()
