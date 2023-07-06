
from django.views.generic import CreateView
from core.producto.forms import SaleForm

from core.producto.models import Sale

from django.contrib.auth.mixins import LoginRequiredMixin
from core.producto.mixins import ValidatePermissionRequiredMixin

from django.http import JsonResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class SaleCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Sale
    form_class = SaleForm
    template_name= 'sale/create.html'
    success_url = reverse_lazy('producto:Categoria_list')
    permission_required = 'producto.add_sale'

    @method_decorator(csrf_exempt)
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
        context['titulo'] = 'Creación de Ventas'
        context['entity'] = 'add'
        context['list_url'] = self.success_url
        return context    