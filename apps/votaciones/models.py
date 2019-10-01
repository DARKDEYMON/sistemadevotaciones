from django.db import models
from django.db.models import Count, Min, Sum, Avg
import math

# Create your models here.

class eleccion(models.Model):
	nombre_eleccion = models.CharField(
		max_length=60,
		blank=False,
		null=False
	)
	descripcion = models.TextField(
		blank=True,
		null=True
	)
	def total(self):
		res = self.mesa_set.filter(eleccion=self)
		t=0
		for a in res:
			t=t+a.total()
		return t
	def total_nulos(self):
		res = self.mesa_set.filter(eleccion=self)
		t=0
		for a in res:
			t=t+a.nulos
		return t
	def pocen_nulos(self):
		return (self.total_nulos()/self.total())*100
	def total_blancos(self):
		res = self.mesa_set.filter(eleccion=self)
		t=0
		for a in res:
			t=t+a.blancos
		return t
	def pocen_blancos(self):
		return (self.total_blancos()/self.total())*100
	def __str__(self):
		return self.nombre_eleccion

class partidos(models.Model):
	eleccion = models.ForeignKey(eleccion, on_delete=models.CASCADE)
	nombre_partido = models.CharField(
		max_length=60,
		blank=False,
		null=False
	)
	def total_votos(self):
		return self.votos_set.aggregate(suma=Sum('votos'))['suma']
	def total_pocen(self):
		return (self.total_votos()/self.eleccion.total())*100
	def __str__(self):
		return self.nombre_partido

class mesa(models.Model):
	eleccion = models.ForeignKey(eleccion, on_delete=models.CASCADE)
	mesa = models.IntegerField(
		null=False,
		blank=False
	)
	nulos = models.IntegerField(
		null=False,
		blank=False
	)
	blancos = models.IntegerField(
		null=False,
		blank=False
	)
	def total(self):
		res = self.votos_set.aggregate(suma=Sum('votos'))['suma'] + self.nulos + self.blancos
		return res
	def porcentaje_nulos(self):
		return ((self.nulos / self.total()) *100)
	def porcentaje_blancos(self):
		return ((self.blancos / self.total()) *100)
	def __str__(self):
		return str(self.mesa)
	class Meta:
		unique_together = (('eleccion', 'mesa'),)

class votos(models.Model):
	mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
	partidos = models.ForeignKey(partidos, on_delete=models.CASCADE)
	votos = models.IntegerField(
		null=False,
		blank=False
	)
	def pocentaje(self):
		return ((self.votos / self.mesa.total()) *100)
	class Meta:
		unique_together = (('mesa', 'partidos'),)
	def __str__(self):
		return str(self.mesa) +str(self.partidos)