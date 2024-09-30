from .models import project
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializers

class projectViewSet(viewsets.ModelViewSet):
    queryset = project.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializers