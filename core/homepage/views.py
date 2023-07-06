from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'homepage/index.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('producto:Producto_list')
        context['list_url_categoria'] = reverse_lazy('producto:Categoria_list')
        # context["Producto"] = 'Producto_list'
        return context
    
