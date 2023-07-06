from typing import Any
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import redirect
from django.views.generic import RedirectView

from Mercurio.settings import LOGIN_REDIRECT_URL
# import config.settings as setting


# Create your views here.

class TierraLoginFormView (LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
class TierraLogoutForm(RedirectView):
    # redirecionar al login con pattern_name
    pattern_name = 'login'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        # se ejecuta esto y se redirecciona a pattern_name: login
        logout(request)
        return super().dispatch(request, *args, **kwargs)