from django.db import models


# Create your models here.
class Province(models.Model):
    nombre_prov = models.CharField(max_length=255, help_text="Introduce tu provincia", unique= True, verbose_name="Nombre Provincia")
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_actual = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre_prov
