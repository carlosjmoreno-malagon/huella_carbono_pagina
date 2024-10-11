from django.urls import path
from .views import PrediccionAIView

urlpatterns = [
    path('prediccion/', PrediccionAIView.as_view(), name='prediccion_ia'),
]