from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from core.producto.forms import CategoriaFrom
from core.producto.mixins import IsSuperUserMixin, ValidatePermissionRequiredMixin
from core.producto.models import categoria
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# El IsSuperUserMixin deben de ir primero para que tenga mas prioridad antes que su vista generica
# El LoginRequiredMixin es para validar si un usuario está registrado, hace la misma funcion que el decorador @method_decorator(login_required)
class CategoriaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin , ListView): #
    model = categoria
    template_name = 'categoria/list.html'
    permission_required = 'producto.edit_categoria'
    # url_redirect_return = reverse_lazy('producto:Producto_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']

            if action == 'productodata':
                data = []
                for i in categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error']='Ocurrio un problema en obtener los datos de categorias'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Categorias'
        context['create_url'] = reverse_lazy('producto:Categoria_create')
        return context
    
class CategoriaCreateView(CreateView):
    model = categoria
    form_class = CategoriaFrom
    template_name= 'categoria/create.html'
    success_url = reverse_lazy('producto:Categoria_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'Se ha producido un error al crear una categoria'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    
    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creación de Categoria'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('producto:Categoria_list')
        return context    

class CategoriaUpdateView(UpdateView):
    model = categoria
    template_name='categoria/create.html'
    form_class= CategoriaFrom
    success_url=reverse_lazy('producto:Categoria_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error']='Error al actualizar datos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de la Categoria'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('producto:Categoria_list')
        return context    

class CategoriaDeleteView(DeleteView):
    model = categoria
    template_name = 'categoria/delete.html'
    success_url = reverse_lazy('producto:Categoria_delete')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as a:
            data['errot'] = 'Ha ocurrido un error al eliminar la categoria'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminación de una Categoria'
        context['list_url'] = reverse_lazy('producto:Categoria_list')
        return context     