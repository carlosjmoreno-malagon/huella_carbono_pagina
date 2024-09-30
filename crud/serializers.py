from rest_framework import serializers
from .models import project


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ('id', 'title','description','technology','created_at')
        read_only_fields = ('created_at',)