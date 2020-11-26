from django.contrib import admin
from pages.models import Categoria, Post

# Register your models here.
admin.site.register([Categoria, Post])
