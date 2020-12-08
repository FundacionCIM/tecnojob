from django.urls import path
from .views import company_view, company_delete, transition_update, company_update


urlpatterns = [
    path('crear',               company_view,      name="mostrar_empresa"),
    path('eliminar/<int:id>',   company_delete,    name="borrar_empresa"),
    path('actualizar/<int:id>', transition_update, name="modificar_empresa"),
    path('update/<int:id>',     company_update,    name='actualizar_empresa'),
]