"""Endpoints do projeto que já têm modelos compatíveis."""
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, ProjetoViewSet

router = DefaultRouter()
router.register('projetos', ProjetoViewSet, basename='projeto')
router.register('equipes', EquipeViewSet, basename='equipe')

urlpatterns = router.urls
