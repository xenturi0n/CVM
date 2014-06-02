from django.contrib import admin
from apps.elementos.models import Elemento
from django.contrib.admin import ModelAdmin

class CustomElementoAdmin(ModelAdmin):
    list_display =('nombre', 'id','coordinacion', 'subdireccion', 'region', 'agrupamiento','coordinacion_lab', 'subdireccion_lab', 'region_lab', 'agrupamiento_lab')

admin.site.register(Elemento, CustomElementoAdmin)
# Register your models here.
