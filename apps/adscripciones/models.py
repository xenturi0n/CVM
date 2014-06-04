# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey
#from mptt.managers import TreeManager
from django.db.models import F

#TODO: agregar manager personalizado para recuperar todos los elementos
#TODO: implementar funciones para cambiar el orden de un nodo
#TODO: mejorar la pagina del administrador
#TODO: implementar metodos para hacer colapsables los nodo del arbol en el admin
#TODO: mejorar el administrador para mostrar los elementos relacionados a cada
#TODO: investigar como funcionan las SIGNALS para el metodo save
#Todo: Agregar campo para otras adscripciones y toda la logica correspondiene
#Todo: investigar  using F() expressions in queries


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

    #*** METODOS PARA OBTENER ELEMENTOS RELACIONADOS ***********************************
    def elementos_get_laborando_en(self, arbol_completo=False):
        if arbol_completo:
            return self.elementos_laborando_aqui.model.objects.filter\
                (laborando_en__in = self.get_descendants(include_self=True))
        else:
            return self.elementos_laborando_aqui.all()

    def elementos_get_adscritos(self, arbol_completo=False):
        if arbol_completo:
            return self.elementos_adscritos.model.objects.filter\
                (adscripcion__in = self.get_descendants(include_self=True))
        else:
            return self.elementos_adscritos.all()

    def elementos_get_apoyando(self, arbol_completo=False):
        if arbol_completo:
                return self.elementos_adscritos.model.objects.filter\
                    (adscripcion__in = self.get_descendants(include_self=True))\
                    .exclude(adscripcion=F('laborando_en'))
        else:
            return self.elementos_adscritos.exclude(adscripcion=F('laborando_en'))

    def elementos_get_de_apoyo(self, arbol_completo=False):
        if arbol_completo:
                return self.elementos_laborando_aqui.model.objects.filter\
                    (laborando_en__in = self.get_descendants(include_self=True))\
                    .exclude(adscripcion=F('laborando_en'))
        else:
            return self.elementos_laborando_aqui.exclude(adscripcion=F('laborando_en'))
    #************************************************************************************

    #*** METODOS PARA DESPLAZAR ELEMENTOS DEL ARBOL**************************************
    #Todo: Modificar para prevenir error en caso de querer mover solo un nodo sin siblings (hermanos)
    def get_first_sibling(self):
        sibs = self.get_siblings(include_self=True)
        fs=self

        for sib in sibs:
            if sib.lft<fs.lft:
                fs = sib
        return fs

    def get_last_sibling(self):
        sibs = self.get_siblings(include_self=True)
        fs=self

        for sib in sibs:
            if sib.lft>fs.lft:
                fs = sib
        return fs

    def mover_abajo(self):
        if None == self.parent_id:
            return None

        if self.get_next_sibling():
            self.move_to(self.get_next_sibling(), position='right')
        else:
            self.move_to(self.get_first_sibling(), position='left')

        self.__class__.objects.rebuild()

    def mover_arriba(self):
        if None == self.parent_id:
            return None

        if self.get_previous_sibling() and self.parent_id>0:
            self.move_to(self.get_previous_sibling(), position='left')
        else:
            self.move_to(self.get_last_sibling(), position='right')

        self.__class__.objects.rebuild()


    def save(self, *args, **kwargs):
        self.__class__.objects.rebuild()
        super(Adscripcion, self).save(*args,**kwargs)
        self.elementos_laborando_aqui.model.objects.reconstruir_campos()
        self.elementos_adscritos.model.objects.reconstruir_campos()


    def __str__(self):
        return self.nombre_lgo

    def __repr__(self):
        return '%s\n'%self.nombre_cto

    class Meta:
        verbose_name='Adscripcion'
        verbose_name_plural='Adscripciones'



