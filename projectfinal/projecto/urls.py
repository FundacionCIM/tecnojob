from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/', views.home_page_view),
    path('',            include("pages.urls")),
    path('accounts/',   include("autenticacion.urls")),
    path('ofertas/',    include("pages.urls")),
    path('empresas/',   include("company_crud.urls")),
    path('curriculum/', include("cv_crud.urls")),
    path('provincias/', include("province_crud.urls")),
    path('cuidades/',   include("city_crud.urls")),
    # path('candidato/',  include("candidate_crud.urls")),
]
