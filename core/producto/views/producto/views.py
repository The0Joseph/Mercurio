from django.http import JsonResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from core.producto.models import producto
from django.views.generic import ListView, CreateView,UpdateView, DeleteView, FormView
from core.producto.forms import ProductoForm

class TierraListView(ListView):
    model = producto
    template_name = 'producto/list.html'
    context_object_name = 'productos'

    # Esta funcion se ejecuta primero

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print(self.request.GET)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in producto.objects.all():
                    data.append(i.toJSON())
                    # print(i)
                    # print(data)
            else:
                data['error'] = 'Ha ocurrido un error no se ha encontrado action: searchdata'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('producto:Producto_add')
        context['list_url'] = reverse_lazy('producto:Producto_list')
        context['list_url_categoria'] = reverse_lazy('producto:Categoria_list')
        return context

class TierraCreateView(CreateView):
    # Modelo a usar
    model = producto
    # Formulario a usar, este llama a un funcion creada en el archivo form.py
    form_class = ProductoForm
    # Template de la vista a cual se va tener que crear el form
    template_name = 'producto/create.html'
    # Se redirecciona cuando se haga el registro completo / Reverse_lazy (manda un url, traduce una cadena)
    success_url = reverse_lazy('producto:Producto_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                # print(form)
                data = form.save()
                # print(data)
            else:
                data['error'] = 'No hay action para add line 50'
                
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    #     print(request)
    #     print(request.POST)
    #     formulario = CategoriaForm(request.POST)
    #     if formulario.is_valid():
    #         formulario.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['formulario'] = formulario
    #     return render(request, self.template_name, context)

        # return super().post(request, *args, **kwargs)

    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creación del Producto'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('producto:Producto_list')
        return context    

class TierraUpdateView(UpdateView):
    # Modelo a usar
    model = producto
    # Formulario a usar, este llama a un funcion creada en el archivo form.py
    form_class = ProductoForm
    # Template de la vista a cual se va tener que crear el form
    template_name = 'producto/create.html'
    # Se redirecciona cuando se haga el registro completo / Reverse_lazy (manda un url, traduce una cadena)
    success_url = reverse_lazy('producto:Producto_list')

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
                # print(self.get_form())
                data = form.save()
            else:
                data['error'] = 'No hay action para add line 106: Producto'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición del Producto'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('producto:Producto_list')
        return context       

class TierraDeleteView(DeleteView):
    model = producto
    template_name = 'producto/delete.html'
    success_url = reverse_lazy('producto:Producto_list')

    # @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminación de un Producto'
        context['list_url'] = reverse_lazy('producto:Producto_list')
        return context     

class TierraFormView(FormView):
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('producto:Producto_list')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Form | Productos'
        context['create_url'] = reverse_lazy('producto:Producto_add')
        context['list_url'] = reverse_lazy('producto:Producto_list')
        return context