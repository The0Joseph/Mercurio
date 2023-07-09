
import json
from django.views.generic import CreateView, ListView
from core.producto.forms import SaleForm

from core.producto.models import Sale, producto, DetSale

from django.contrib.auth.mixins import LoginRequiredMixin
from core.producto.mixins import ValidatePermissionRequiredMixin

from django.http import JsonResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.db import transaction


class SaleListView(ListView):
    model = Sale
    template_name = "sale/list.html"
    
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']
            if action == 'salesData':
                data =[]
                for i in Sale.objects.all():
                    data.append(i.toJSON())
                # print(data)
            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
            data['error'] = 'Ha ocurrido un error en mostrar la lista de datos de ventas' . str(e)
            
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('producto:Venta_list')
        context['create_url'] = reverse_lazy('producto:Venta_create')
        return context 
    



class SaleCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Sale
    form_class = SaleForm
    template_name= 'sale/create.html'
    success_url = reverse_lazy('producto:Venta_list')
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
                with transaction.atomic():
                    verts = json.loads(request.POST['verts']) #Convertir str a json con loads
                    # print(verts)

                    sale = Sale()
                    sale.date_joined = verts['date_joined']
                    sale.cli_id = verts['cli']
                    sale.subtotal = float(verts['subtotal'])
                    sale.iva = float(verts['iva'])
                    sale.total = float(verts['total'])
                    sale.save()

                    #Iterando los productos 
                    for i in verts['productos']:
                        detalleVenta = DetSale()
                        detalleVenta.sale_id = sale.id
                        detalleVenta.prod_id = i['id']
                        detalleVenta.price = float(i['pvp'])
                        detalleVenta.cant = int(i['cant'])
                        detalleVenta.subtotal = float(i['subtotal'])
                        detalleVenta.save()

            elif action == 'searchProductos':
                data=[]
                productosFilter = producto.objects.filter(name__icontains=request.POST['term'])
                for i in productosFilter[0:1]:
                    productoJson = i.toJSON()
                    productoJson['text'] = i.name
                    data.append(productoJson)
                    # data.append({
                    #     'id':i.id,
                    #     'text':i.name
                    # })
            else:
                data['error'] = 'Se ha producido un error al crear una categoria'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
    
    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creación de Ventas'
        context['action'] = 'add'
        context['list_url'] = self.success_url
        return context    