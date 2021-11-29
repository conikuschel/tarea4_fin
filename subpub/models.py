from django.db import models
# Create your models here.

class Transaccion(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    tipo = models.CharField(max_length=100)
    banco_origen = models.IntegerField()
    cuenta_origen = models.IntegerField()
    banco_destino = models.IntegerField()
    cuenta_destino = models.IntegerField()
    monto = models.IntegerField()
    message_id = models.CharField(max_length=100)
