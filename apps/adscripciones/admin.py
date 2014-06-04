from django.contrib import admin
from .models import Adscripcion, TipoAdscripcion
from mptt.admin import MPTTModelAdmin
from CVM import settings

IS_BOOTSTRAPPED_INSTALLED = 'django_admin_bootstrapped' in settings.INSTALLED_APPS

class CustMPTTModelAdmin(MPTTModelAdmin):



    list_display =('nombre_lgo', 'id', 'lft', 'rght', 'parent')
    actions = ['subir_nodo','bajar_nodo']
    mptt_level_indent=20

    def subir_nodo (self, request, queryset):
        c = 0
        for n in queryset:
            n.mover_arriba()
            c+=1
        return c
    subir_nodo.short_description = "Subir elementos seleccionados"

    def bajar_nodo(self, request, queryset):
        c=0
        for n in queryset:
            n.mover_abajo()
            c+=1
        return c
    bajar_nodo.short_description="Bajar elementos seleccionados"



admin.site.register(Adscripcion, CustMPTTModelAdmin)
admin.site.register(TipoAdscripcion)