from django.shortcuts import render
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import *

# Create your views here.

class eleccionCreate(CreateView):
	form_class = eleccionForm
	template_name = 'form.html'
	success_url = reverse_lazy('votacion:mainelecciones')

class partidosCreate(CreateView):
	form_class = partidosForm
	template_name = 'form.html'
	success_url = reverse_lazy('votacion:mainelecciones')
	def get_context_data(self, **kwargs):
		#print (self.kwargs)
		get_object_or_404(eleccion,pk = self.kwargs.get('pk',0))
		return super(partidosCreate, self).get_context_data(**kwargs)
	def post(self, request, *args, **kwargs):
		self.object = self.get_object	
		form = self.form_class(data=request.POST)
		if form.is_valid():
			pre = form.save(commit=False)
			pk = self.kwargs.get('pk',0)
			pre.eleccion = eleccion.objects.get(pk=pk)
			form.save()
			return  HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

class votoView(CreateView):
	form_class = formVoto
	template_name = 'index.html'
	success_url = 'votacion:inservota'
	def get_context_data(self, **kwargs):
		#print (self.kwargs)
		if 'form' not in kwargs:
			kwargs['form'] = self.form_class(pk=self.kwargs.get('pk',0))
		return super(votoView, self).get_context_data(**kwargs)
	def get_success_url(self):
		print(self)
		print(self.kwargs.get('pk',0))
		return reverse(self.success_url, kwargs = {'pk': self.kwargs.get('pk',0)})#self.get_object().proyecto.pk
	def post(self, request, *args, **kwargs):
		self.object = self.get_object	
		form = self.form_class(data=request.POST,pk = self.kwargs.get('pk',0))
		if form.is_valid():
			form.save()
			return  HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

class votoViewUpdate(UpdateView):
	model = mesa
	form_class = formVotoUpdate
	template_name = 'index.html'
	success_url = '/'#reverse_lazy('votacion:inservota')


class listaMesa(ListView):
	model = mesa
	template_name = 'tabla_mesas.html'
	paginate_by = 10
	def get_context_data(self, **kwargs):
		#print (self.kwargs)
		if 'id' not in kwargs:
			kwargs['id'] = self.kwargs.get('pk',0)
		return super(listaMesa, self).get_context_data(**kwargs)
	def get_queryset(self):
		print(self.kwargs)
		return  self.model.objects.filter(eleccion__id=self.kwargs['pk'])

class listaEstado(listaMesa):
	template_name = 'estadolec.html'

class listaElecciones(ListView):
	model = eleccion
	template_name = 'tabla_eleciones.html'
	paginate_by = 10