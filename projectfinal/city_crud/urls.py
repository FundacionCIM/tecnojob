from django.urls import path
from .views import city_view, city_delete, transition_update, city_update


urlpatterns = [
    path('crear',               city_view,      name="mostrar_empresa"),
    path('eliminar/<int:id>',   city_delete,    name="borrar_empresa"),
    path('actualizar/<int:id>', transition_update, name="modificar_empresa"),
    path('update/<int:id>',     city_update,    name='actualizar_empresa')
]