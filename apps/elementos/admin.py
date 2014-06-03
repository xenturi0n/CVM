from django.contrib import admin
from apps.elementos.models import Elemento
from django.contrib.admin import ModelAdmin

class CustomElementoAdmin(ModelAdmin):
    list_display =('nombre', 'id',\
                   'subdireccion', 'region','agrupamiento',\
                   'subdireccion_lab', 'region_lab', 'agrupamiento_lab',\
                   'de_apoyo',)

admin.site.register(Elemento, CustomElementoAdmin)
# Register your models here.
