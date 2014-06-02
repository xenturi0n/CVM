# -*- coding: utf-8 -*-
from django.db import models
from apps.adscripciones.models import Adscripcion
from django.utils.encoding import python_2_unicode_compatible


class MixinElemento(object):
#TODO: probar con nombre corto para detallar la adscripcion en lugar de nobre largo
#Todo: generar un campo automatico para saber si el elemento esta de apoyo
    @staticmethod
    def detallar_adscripcion(elemento):
        ancestro=elemento.adscripcion.get_ancestors(include_self=True)
        if 0< len(ancestro):
            elemento.coordinacion=ancestro[0].nombre_cto
        else:
            elemento.coordinacion='Comandancia'

        if 1< len(ancestro):
            elemento.subdireccion=ancestro[1].nombre_cto
        else:
            elemento.subdireccion='Comandancia'

        if 2< len(ancestro):
            elemento.region=ancestro[2].nombre_cto
        else:
            elemento.region='Comandancia'

        if 3< len(ancestro):
            elemento.agrupamiento=ancestro[3].nombre_cto
        else:
            elemento.agrupamiento='Comandancia'

        ancestro=elemento.laborando_en.get_ancestors(include_self=True)

        if 0< len(ancestro):
            elemento.coordinacion_lab=ancestro[0].nombre_cto
        else:
            elemento.coordinacion_lab='Comandancia'

        if 1< len(ancestro):
            elemento.subdireccion_lab=ancestro[1].nombre_cto
        else:
            elemento.subdireccion_lab='Comandancia'

        if 2< len(ancestro):
            elemento.region_lab=ancestro[2].nombre_cto
        else:
            elemento.region_lab='Comandancia'

        if 3< len(ancestro):
            elemento.agrupamiento_lab=ancestro[3].nombre_cto
        else:
            elemento.agrupamiento_lab='Comandancia'


class ElementoManager(models.Manager):
        def reconstruir_adscripcion_path(self):
            elementos = self.all()
            for e in elementos:
                MixinElemento.detallar_adscripcion(e)
                e.save()

@python_2_unicode_compatible
class Elemento (models.Model):
    nombre = models.CharField(max_length=255)
    adscripcion = models.ForeignKey(Adscripcion, related_name='elementos_adscritos')
    laborando_en = models.ForeignKey(Adscripcion, related_name='elementos_laborando_aqui')

    objects = models.Manager()
    Emanager=ElementoManager()

    """
        Estos camps son autogenerados en base a los ancestros del campo adscripcion
        y representan la adscripcion oficial del elemento.
    """
    coordinacion = models.CharField(max_length=60, blank=True)
    subdireccion = models.CharField(max_length=60, blank=True)
    region = models.CharField(max_length=60, blank=True)
    agrupamiento = models.CharField(max_length=60, blank=True)

    """
        Estos campost tambien son autogenerados en base a los ancestros del campo
        laborando_en y representan en donde se encuentra laborando fisicamente
        el elemento.
    """
    coordinacion_lab = models.CharField(max_length=60, blank=True)
    subdireccion_lab = models.CharField(max_length=60, blank=True)
    region_lab = models.CharField(max_length=60, blank=True)
    agrupamiento_lab = models.CharField(max_length=60, blank=True)

    def save(self, *args, **kwargs):
        MixinElemento.detallar_adscripcion(self)
        super(Elemento, self).save(*args,**kwargs)

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return 'nombre: %s\t%s\t%s\t%s\t%s\t%s\n'%\
               (self.nombre,self.coordinacion,self.subdireccion,self.region,self.agrupamiento,self.laborando_en)
