from django.shortcuts import render
from django.http import HttpResponse
from base64 import b64decode, b64encode
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from subpub.serializers import TransaccionSerializer, ConciliacionSerializer
from subpub.models import Transaccion, Conciliacion

# Create your views here.

def home(request):
    trans = Transaccion.objects.all().values()
    transi = Conciliacion.objects.all().values()
    lista=[]
    lista.append(trans)
    lista.append(transi)
    return render(request, 'home.html', {'response':lista})

@api_view(['POST'])
def recibir_transaccion(request):
    if request.method == "POST":
        algo = request.data['message']
        message = algo['messageId']
        fecha = algo['publishTime']
        try:
            Transaccion.objects.get(message_id = message)
        except Transaccion.DoesNotExist:
            algo = algo["data"]
            ver = b64decode(algo.encode()) 
            ver = str(ver)
            ver = ver[2:]
            if len(ver) == 65:
                tipo = ver[0:4]
                ide = ver[4:14]
                ban_origen = int(ver[14:21])
                cuen_origen = int(ver[21:31])
                ban_dest = int(ver[31:38])
                cuen_dest = int(ver[38:48])
                monto = int(ver[48:64])
                transac = {"tipo": tipo, "id": ide, "banco_origen":ban_origen, "cuenta_origen": cuen_origen, 
                    "banco_destino":ban_dest, "cuenta_destino":cuen_dest, "monto":monto, "message_id":message, "fecha":fecha}
                serializer = TransaccionSerializer(data=transac, many=False)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            if ban_origen != ban_dest:
                try:
                    conci = Conciliacion.objects.get(banco_origen = ban_origen, banco_destino = ban_dest)
                    monti = conci.montos
                    if tipo == "2200":
                        monti += monto
                    elif tipo == "2400":
                        monti -= monto
                    conci.montos = monti
                    conci.save()
                except Conciliacion.DoesNotExist:
                    try:
                        conci = Conciliacion.objects.get(banco_destino = ban_origen, banco_origen = ban_dest)
                        monti = conci.montos
                        if tipo == "2200":
                            monti -= monto
                        elif tipo == "2400":
                            monti += monto
                        conci.montos = monti
                        conci.save()
                    except Conciliacion.DoesNotExist:
                        if tipo == "2200":
                            transac = {"banco_origen":ban_origen,"banco_destino":ban_dest,"montos":monto}
                            serializer = ConciliacionSerializer(data=transac, many=False)

                            if serializer.is_valid():
                                serializer.save()
                            else:
                                print(serializer.errors)
                        elif tipo == "2400":
                            monto = -monto
                            transac = {"banco_origen":ban_origen,"banco_destino":ban_dest,"montos":monto}
                            serializer = ConciliacionSerializer(data=transac, many=False)

                            if serializer.is_valid():
                                serializer.save()
                            else:
                                print(serializer.errors)

    return Response(status=status.HTTP_200_OK)