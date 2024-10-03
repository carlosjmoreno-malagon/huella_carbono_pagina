from .models import Project
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializer  # Asegúrate de que el nombre sea correcto

class ProjectViewSet(viewsets.ModelViewSet):  # Cambia a PascalCase
    queryset = Project.objects.all()  # Cambia a PascalCase
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer  # Cambia a PascalCase
