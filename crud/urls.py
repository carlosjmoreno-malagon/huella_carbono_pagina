from rest_framework import routers
from .api import projectViewSet
router = routers.DefaultRouter()
router.register('api/crud', projectViewSet, 'crud')

urlpatterns = router.urls