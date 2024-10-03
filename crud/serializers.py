from rest_framework import serializers
from .models import Project  # Asegúrate de usar el nombre correcto

class ProjectSerializer(serializers.ModelSerializer):  # Cambia a PascalCase
    class Meta:
        model = Project  # Cambia a PascalCase
        fields = ('id', 'title', 'description', 'technology', 'created_at')
        read_only_fields = ('created_at',)
