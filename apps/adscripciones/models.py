# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from django.db.models import F

#TODO: agregar manager personalizado para recuperar todos los elementos
#TODO: implementar funciones para cambiar el orden de un nodo
#TODO: mejorar la pagina del administrador
#TODO: implementar metodos para hacer colapsables los nodo del arbol en el admin
#TODO: mejorar el administrador para mostrar los elementos relacionados a cada
#TODO: investigar como funcionan las SIGNALS para el metodo save
#Todo: Agregar campo para otras adscripciones y toda la logica correspondiene
#Todo: investigar  using F() expressions in queries

class MixinAdscripcion(object):
    #@staticmethod
    #def mover_nodo_arriba(nodo):


    #@staticmethod
    #def mover_nodo_abajo(nodo):

    @staticmethod
    def obtener_elementos(nodos):
        return Adscripcion.elementos_laborando_aqui.filter(laborando_en__in=nodos)


class Amanager(TreeManager):
    def get_elementos_subordinados(self):
        return super(Amanager, self).get_ancestors(self)


@python_2_unicode_compatible
class TipoAdscripcion(models.Model):
    tipo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name= 'Tipo de Ascripcion'
        verbose_name_plural = 'Tipos de Adscripcion'


@python_2_unicode_compatible
class Adscripcion (MPTTModel):
    nombre_lgo = models.CharField(max_length=255, blank=True)
    nombre_cto = models.CharField(max_length=255, blank=True)
    tipo = models.ForeignKey(TipoAdscripcion, related_name='adscripciones', blank=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    elemanager =Amanager()

    def get_laborando_en(self):
        return self.elementos_laborando_aqui.model.objects.filter\
            (laborando_en__in = self.get_descendants(include_self=True))

    def get_adscritos(self):
        return self.elementos_adscritos.model.objects.filter\
            (adscripcion__in = self.get_descendants(include_self=True))

    def get_laborando_fuera(self):
        return self.elementos_adscritos.model.objects.filter\
            (adscripcion__in = self.get_descendants(include_self=True))\
            .exclude(adscripcion=F('laborando_en'))

    def __str__(self):
        return self.nombre_lgo

    def __repr__(self):
        return '%s\n'%self.nombre_cto

    class Meta:
        verbose_name='Adscripcion'
        verbose_name_plural='Adscripciones'



