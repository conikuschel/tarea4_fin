from django.db import models
# Create your models here.

class Transaccion(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    tipo = models.CharField(max_length=100)
    banco_origen = models.CharField(max_length=100)
    cuenta_origen = models.CharField(max_length=100)
    banco_destino = models.CharField(max_length=100)
    cuenta_destino = models.CharField(max_length=100)
    monto = models.IntegerField()
