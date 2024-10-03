from rest_framework import routers
from .api import ProjectViewSet  # Cambia a PascalCase

router = routers.DefaultRouter()
router.register('api/crud', ProjectViewSet, basename='crud')  # Cambia a 'basename' en lugar de 'crud'

urlpatterns = router.urls
