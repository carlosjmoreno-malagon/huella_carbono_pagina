from django.db import models

class project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    