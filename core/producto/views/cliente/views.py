from datetime import datetime
from core.producto.models import Client
from core.producto.forms import ClienteForm
# Vista Generica
from django.views.generic import TemplateView

from django.http import JsonResponse
from django.urls import reverse_lazy
# Decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class ClientView(TemplateView):
    model = Client
    template_name = 'cliente/list.html'


    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']

            if action == 'searchdata':
                data = []
                for i in Client.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':

                try:
                    form = ClienteForm(request.POST)
                    # fecha_birthday = datetime.strptime(i['date_birthday'], '%d-%m-%Y')
                    # print(fecha_birthday)
                    # form.date_birthday = datetime.strftime(fecha_birthday, '%Y-%m-%d')
                    # print(form.date_birthday)
                    data = form.save()
                except Exception as e:
                    print(str(e))

                
            elif action == 'edit':

                try:
                    cli = Client.objects.get(pk=request.POST.get('id'))
                    form = ClienteForm(request.POST, instance = cli)
                    data = form.save()
                except Exception as e:
                    print(str(e))

            elif action == 'delete':

                try:
                    cli = Client.objects.get(pk=request.POST.get('id'))
                    # form = ClienteForm(request.POST, instance = cli)
                    # data = form.save()
                    cli.delete()
                except Exception as e:
                    print(str(e))                    

                
            else:
                data['error']='Ocurrio un problema en obtener los datos del cliente'
        except Exception as e:
            data['error']=str(e)
        
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Clientes'
        context['list_url'] = reverse_lazy('producto:cliente')
        context['entity'] = 'Clientes'
        context['form'] = ClienteForm()
        return context    

