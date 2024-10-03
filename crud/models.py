from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crud_project'  # Nombre de la tabla en la base de datos

    def __str__(self):
        return self.title  # Representación legible del objeto
