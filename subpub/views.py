from django.shortcuts import render
from django.http import HttpResponse
from base64 import b64decode, b64encode
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from subpub.serializers import TransaccionSerializer
from subpub.models import Transaccion

# Create your views here.

def home(request):
    trans = Transaccion.objects.all().values()
    print(trans)
    return render(request, 'home.html', {'response':trans})

@api_view(['POST'])
def recibir_transaccion(request):
    if request.method == "POST":
        algo = request.data['message']
        message = algo['messageId']
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
                print(tipo,ide,ban_origen,cuen_origen, ban_dest,cuen_dest,monto)
                transac = {"tipo": tipo, "id": ide, "banco_origen":ban_origen, "cuenta_origen": cuen_origen, 
                    "banco_destino":ban_dest, "cuenta_destino":cuen_dest, "monto":monto, "message_id":message}
                serializer = TransaccionSerializer(data=transac, many=False)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
    return Response(status=status.HTTP_200_OK)