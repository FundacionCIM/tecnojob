from django.urls import path
from .views import province_view, province_delete, p_transition_update, province_update


urlpatterns = [
    path('crear',               province_view,      name="mostrar_provincia"),
    path('eliminar/<int:id>',   province_delete,    name="borrar_provincia"),
    path('actualizar/<int:id>', p_transition_update,  name="modificar_provincia"),
    path('update/<int:id>',     province_update,    name='actualizar_provincia'),
]