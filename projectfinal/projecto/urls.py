from django.contrib import admin
from django.urls import path, include
from pages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/', views.home_page_view),
    path('', include("pages.urls")),
    path('accounts/', include("autenticacion.urls")),
    path('ofertas/', include("pages.urls")),
]
