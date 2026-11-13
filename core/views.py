from rest_framework import viewsets
from .models import Vendedor, Cliente
from .serializers import VendedorSerializer, ClienteSerializer
from django_filters.rest_framework import DjangoFilterBackend 

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ClienteViewSet(viewsets.ModelViewSet):
        queryset = Cliente.objects.all()
        serializer_class = ClienteSerializer
        
