from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    nombre_cat    = models.CharField(max_length=255, unique=True, verbose_name="Nombre categoria")
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_actual  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre_cat

    class Meta:
        db_table: 'category'
        verbose_name: 'Categoria'
        verbose_name_plural: 'Categorias'
        ordering: [id]


