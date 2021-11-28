from django.shortcuts import render
from django.http import HttpResponse
from base64 import b64encode
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from subpub.models import Transaccion

# Create your views here.

def home(request):
    trans = Transaccion.objects.all().values()
    print(trans)
    return render(request, 'home.html', {'response':trans})

@api_view(['POST'])
def recibir_transaccion(request):
    if request.method == "POST":
        print(request.data)
        print("llegoo")
    return Response(status=status.HTTP_200_OK)