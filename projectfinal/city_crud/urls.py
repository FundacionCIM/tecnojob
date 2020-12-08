from django.urls import path
from .views import city_view, city_delete, c_transition_update, city_update


urlpatterns = [
    path('crear',               city_view,           name="mostrar_ciudad"),
    path('eliminar/<int:id>',   city_delete,         name="borrar_ciudad"),
    path('actualizar/<int:id>', c_transition_update, name="modificar_ciudad"),
    path('update/<int:id>',     city_update,         name='actualizar_ciudad')
]