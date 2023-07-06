from django.urls import path
from core.login.views import *

urlpatterns = [
    path('', TierraLoginFormView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout')
    path('logout/', TierraLogoutForm.as_view(), name='logout')
]