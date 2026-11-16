"""ViewSets ligados aos modelos Django existentes."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Equipe, Projeto
from .serializers import EquipeSerializer, ProjetoSerializer


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all().order_by('id')
    serializer_class = ProjetoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all().order_by('id')
    serializer_class = EquipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
