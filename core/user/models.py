from django.db import models
from django.contrib.auth.models import AbstractUser

from Mercurio.settings import MEDIA_URL, STATIC_URL

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='Users', null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/Dado.png')