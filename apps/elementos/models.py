# -*- coding: utf-8 -*-
from django.db import models
from apps.adscripciones.models import Adscripcion
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import TreeForeignKey

#TODO: probar con nombre corto para detallar la adscripcion en lugar de nobre largo
#Todo: generar un campo automatico para saber si el elemento esta de apoyo


class ManagerElemento(models.Manager):
        def reconstruir_campos(self):
            elementos = self.all()
            for e in elementos:
                e.save()

@python_2_unicode_compatible
class Elemento (models.Model):
    nombre = models.CharField(max_length=255)
    adscripcion = TreeForeignKey(Adscripcion, related_name='elementos_adscritos')
    laborando_en = TreeForeignKey(Adscripcion, related_name='elementos_laborando_aqui')
    coordinacion = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    subdireccion = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    region = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    agrupamiento = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    coordinacion_lab = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    subdireccion_lab = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    region_lab = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    agrupamiento_lab = models.CharField(max_length=60, blank=True) #campo calculado antes de guardar
    de_apoyo = models.BooleanField(default=False) #campo calculado antes de guardar


    objects = ManagerElemento()

    #Esta funcion es horrible pero no he encotrado una forma de hacerla mas elegante
    def detallar_adscripcion(self):
        ancestros=self.adscripcion.get_ancestors(include_self=True)
        if 0< len(ancestros):
            self.coordinacion=ancestros[0].nombre_cto
        else:
            self.coordinacion='Comandancia'

        if 1< len(ancestros):
            self.subdireccion=ancestros[1].nombre_cto
        elif len(ancestros)==1:
            self.subdireccion=ancestros[0].nombre_cto
        else:
            self.subdireccion='Comandancia'

        if 2< len(ancestros):
            self.region=ancestros[2].nombre_cto
        else:
            self.region='Comandancia'

        if 3< len(ancestros):
            self.agrupamiento=ancestros[3].nombre_cto
        else:
            self.agrupamiento='Comandancia'

        ancestros=self.laborando_en.get_ancestors(include_self=True)

        if 0< len(ancestros):
            self.coordinacion_lab=ancestros[0].nombre_cto
        else:
            self.coordinacion_lab='Comandancia'

        if 1< len(ancestros):
            self.subdireccion_lab=ancestros[1].nombre_cto
        elif len(ancestros)==1:
            self.subdireccion_lab=ancestros[0].nombre_cto
        else:
            self.subdireccion_lab='Comandancia'

        if 2< len(ancestros):
            self.region_lab=ancestros[2].nombre_cto
        else:
            self.region_lab='Comandancia'

        if 3< len(ancestros):
            self.agrupamiento_lab=ancestros[3].nombre_cto
        else:
            self.agrupamiento_lab='Comandancia'


    def set_de_apoyo(self):
        if self.adscripcion == self.laborando_en:
            self.de_apoyo=False
        else:
            self.de_apoyo=True

    def save(self, *args, **kwargs):
        self.detallar_adscripcion()
        self.set_de_apoyo()
        super(Elemento, self).save(*args,**kwargs)

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return 'nombre: %s\t%s\t%s\t%s\t%s\t%s\n'%\
               (self.nombre,self.coordinacion,self.subdireccion,self.region,self.agrupamiento,self.laborando_en)
