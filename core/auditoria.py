from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_update', null=True, blank=True)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        # con el abstract estoy diciendo que este modelo no se va crear en mi tabla, si no se va utilizar para implementar
        # en otras entidades(Tablas) y se va implementar en la tabla categorya que va pasar como parametro
        # de models.Model a BaseModel
        abstract = True