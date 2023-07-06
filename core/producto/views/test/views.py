
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from core.producto.forms import TestForm
from core.producto.models import producto, categoria

class TestListView(TemplateView):
    # model = producto
    template_name = 'test.html'
    # context_object_name = 'productos'

    # Esta funcion se ejecuta primero

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product':
                # se agrego contenido al data porque el select; presentado por ajax no va tener un valor
                data = [{'id':'','text':'-------------'}]
                for i in producto.objects.filter(categoria_foreign_id=request.POST['id']):
                    data.append({
                        'id': i.id,
                        'text': i.name
                    })
                # Se camabio de 'name': i.name a 'text': i.name porque el select pide que para que se lea sea text obligatoriamente
            elif action == 'autocomplete'                :
                data = []
                for i in categoria.objects.filter(name__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error no se ha encontrado action: autocomplete'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Esta funcion te permite agregar datos presentado en pantalla
    def get_context_data(self,**kwargs):
        context = super().get_context_data( **kwargs)
        context['titulo'] = 'Select Anidados'
        context['list_url'] = reverse_lazy('producto:Categoria_list')
        context['form'] = TestForm()
        # context['back_url'] = redirect(request.META.get('HTTP_REFERER'))
        
        return context
    
    