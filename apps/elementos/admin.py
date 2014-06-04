from django.contrib import admin
from apps.elementos.models import Elemento
from django.contrib.admin import ModelAdmin

#Todo: Agregar Filtros, campos de busqueda y mejorar el css del admin

class CustomElementoAdmin(ModelAdmin):
       list_display =('nombre', 'id',
                   'subdireccion', 'region','agrupamiento',
                   'subdireccion_lab', 'region_lab', 'agrupamiento_lab',
                   'de_apoyo',)

       readonly_fields = ('coordinacion', 'subdireccion','region','agrupamiento','de_apoyo',
                          'coordinacion_lab','subdireccion_lab','region_lab','agrupamiento_lab',)

       fieldsets = ((None,{
           'fields':('nombre','adscripcion','laborando_en',)
       }),('Campos calculados automaticamente',
           {'classes':('collapse',),
            'fields':('coordinacion','subdireccion','region','agrupamiento',
            'coordinacion_lab','subdireccion_lab','region_lab','agrupamiento_lab','de_apoyo',),}))



admin.site.register(Elemento, CustomElementoAdmin)
# Register your models here.
