from django.urls import path
from .views import province_view, province_delete


urlpatterns = [
    path('crear',               province_view,      name="mostrar_provincia"),
    path('eliminar/<int:id>',   province_delete,    name="borrar_empresa"),
    # path('actualizar/<int:id>', transition_update,  name="modificar_empresa"),
    # path('update/<int:id>',     province_update,    name='actualizar_empresa')
]