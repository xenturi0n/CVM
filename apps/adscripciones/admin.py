from django.contrib import admin
from .models import Adscripcion, TipoAdscripcion
from mptt.admin import MPTTModelAdmin

class CustMPTTModelAdmin(MPTTModelAdmin):
    list_display =('nombre_lgo', 'id')
    mptt_level_indent=20

admin.site.register(Adscripcion, CustMPTTModelAdmin)
admin.site.register(TipoAdscripcion)