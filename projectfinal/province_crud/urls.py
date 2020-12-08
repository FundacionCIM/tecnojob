from django.urls import path
from .views import province_view, province_delete, transition_update, province_update


urlpatterns = [
    path('crear',               province_view,      name="mostrar_empresa"),
    path('eliminar/<int:id>',   province_delete,    name="borrar_empresa"),
    path('actualizar/<int:id>', transition_update, name="modificar_empresa"),
    path('update/<int:id>',     province_update,    name='actualizar_empresa')
]