from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


class IsSuperUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context
    
class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect_return = None

    def get_url_redirect(self):
        if self.url_redirect_return is None:
            return reverse_lazy('login')
        return self.url_redirect_return

    def get_permission(self):
        # Si el un str ( string ) convierto en una tupla (Line:23), caso contrario mandar toda la tupla
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_permission()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para ingresar a este módulo')
        return redirect(self.get_url_redirect())
    