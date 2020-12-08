from django.urls import path
from .views import candidate_view, candidate_delete, transition_update, candidate_update


urlpatterns = [
    path('crear',               candidate_view,      name="mostrar_empresa"),
    path('eliminar/<int:id>',   candidate_delete,    name="borrar_empresa"),
    path('actualizar/<int:id>', transition_update,   name="modificar_empresa"),
    path('update/<int:id>',     candidate_update,    name='actualizar_empresa')
]