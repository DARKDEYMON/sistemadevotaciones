from django.forms import ModelForm
from django.forms import widgets
from django import forms
from .models import *
from django.shortcuts import get_object_or_404

class partidosForm(ModelForm):
	class Meta:
		model = partidos
		exclude = ['eleccion']

class eleccionForm(ModelForm):
	class Meta:
		model = eleccion
		exclude = ['']

class formVoto(ModelForm):
	class Meta:
		model = mesa
		exclude = ['eleccion']
	def __init__(self, pk=None , *args, **kwargs):
		super(formVoto, self).__init__(*args, **kwargs)
		#print(str(kwargs.get('instance',None))+"aqui")
		self.updateinstance = kwargs.get('instance', None) == None
		#print(self.updateinstance)
		if kwargs.get('instance', None)==None:
			
			self.pk = pk
			self.eleccion = get_object_or_404(eleccion,pk=self.pk)
			self.res = partidos.objects.filter(eleccion__id=self.pk)
			for a in self.res:
				self.fields[a.nombre_partido] = forms.CharField(widget=widgets.TextInput(attrs={'id': a.id}))
		else:
			self.pk = kwargs.get('instance', None).eleccion.id
			self.eleccion = get_object_or_404(eleccion,pk=self.pk)
			#print(self.pk)
			self.res = partidos.objects.filter(eleccion__id=self.pk)
			for a in self.res:
				resins = a.votos_set.filter(mesa=kwargs.get('instance', None))
				print(resins)
				self.fields[a.nombre_partido] = forms.CharField(widget=widgets.TextInput(attrs={'resins': resins[0].id}),initial=resins[0].votos)

	def clean(self):

		cleaned_data = super(formVoto, self).clean()
		eleccion = self.eleccion#cleaned_data.get("eleccion")
		mesas = cleaned_data.get("mesa")

		#print(mesas)
		#print(eleccion)
		if mesa.objects.filter(eleccion=eleccion, mesa=mesas).exclude(pk=self.instance.id).count() > 0:
			# Only do something if both fields are valid so far.:
				raise forms.ValidationError(
					"ya existe la mesa"
				)

	def save(self):
		if(self.updateinstance):
			#print(self.updateinstance)
			m = super(formVoto, self).save(commit=False)
			m.eleccion = self.eleccion
			m.save()
			data = self.cleaned_data
			#print("pk de inicio")
			#print(self.pk)
			#print (self.res)
			for a in self.res:
				v = self.cleaned_data[a.nombre_partido]
				#print(self.cleaned_data[a.nombre_partido])
				#print(self.fields[a.nombre_partido].widget.attrs)
				modelo = votos(mesa=m,partidos=a,votos=v)
				modelo.save()
			#rue = data.get("rue")
		else:
			m = super(formVoto, self).save()
			#print(m)
			for a in self.res:
				av = votos.objects.get(id=self.fields[a.nombre_partido].widget.attrs['resins'])
				print(av)
				av.votos = self.cleaned_data[a.nombre_partido]
				av.save()
		return m

class formVotoUpdate(formVoto):
	class Meta:
		model = mesa
		exclude = ['eleccion','mesa']