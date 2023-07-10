import json
from django.views.generic import CreateView, ListView, UpdateView, View
from core.producto.forms import SaleForm

from core.producto.models import Sale, producto, DetSale

from django.contrib.auth.mixins import LoginRequiredMixin
from core.producto.mixins import ValidatePermissionRequiredMixin

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.db import transaction

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


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
            
            elif action == 'search_detail_sale':
                data=[]
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())

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
        context['edit_url'] = reverse_lazy('producto:Venta_edit')
        return context 
    



class SaleEditView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Sale
    form_class = SaleForm
    template_name= 'sale/create.html'
    success_url = reverse_lazy('producto:Venta_edit')
    permission_required = 'producto.change_sale'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'edit':
                with transaction.atomic():
                    verts = json.loads(request.POST['verts']) #Convertir str a json con loads
                    # print(verts)

                    sale = self.get_object()
                    # print(sale.detsale_set.all())   
                    sale.date_joined = verts['date_joined']
                    sale.cli_id = verts['cli']
                    sale.subtotal = float(verts['subtotal'])
                    sale.iva = float(verts['iva'])
                    sale.total = float(verts['total'])
                    sale.save()
                    sale.detsale_set.all().delete()


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
            else:
                data['error'] = 'Se ha producido un error al crear una categoria'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
    
    def get_detalle_product(self):
        data=[]
        try:
            for i in DetSale.objects.filter(sale_id = self.get_object().id):
                print(i)
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)

        except Exception as e:
            pass    
        return data
    
    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creación de Ventas'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        context['det'] = json.dumps(self.get_detalle_product()) ##El json.dumps conviertir a formato json
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
        context['det'] = []
        return context    
    

class SaleInvoicePDFview(View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice.html') #ruta del template, y devuelve el objecto a base del template dado
            context = {'title': 'Esto es uan plantilla para el pdf o este es el pdf perra'}
            
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"' #Esto es para descargar el pdf automaticamente
            
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response) # , link_callback=link_callback para archivos estaticos

            return response #Se devuelve un objecto httpresponse
        except Exception as e:
            pass
        return HttpResponse(reverse_lazy('producto:Venta_list'))