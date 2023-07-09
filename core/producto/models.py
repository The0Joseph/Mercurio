from collections.abc import Iterable
from crum import get_current_user
from django.db import models
from django.forms import model_to_dict
from datetime import datetime

from Mercurio.settings import MEDIA_URL, STATIC_URL
from core.auditoria import BaseModel

# Create your models here.

estado_choices = (
    (1, 'Activo'),
    (0, 'Inactivo')
)

gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)


class categoria(BaseModel):
    name = models.TextField(verbose_name='Nombre', max_length=20, unique=True)
    status = models.BooleanField(default=True, choices=estado_choices)

    def __str__(self):
        return self.name
    
    def save(self,force_insert=False, force_update=False, using=None, update_fields=None):

        user=get_current_user()

        # Si el usuario no esta vacio
        if user is not None:
            # Si el usuario no tiene llave primaria (significa que recien hecho una creación)
            if not self.pk:
                self.user_creation = user
            
            # Si el usaurio ya tiene llave primaria
            else:
                self.user_update = user



        return super().save()

    # convertir los datos del objecto categoria en json
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        ordering = ['id']



class producto(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Nombre')
    categoria_foreign = models.ForeignKey(categoria, verbose_name=("Categoria"), on_delete=models.CASCADE)
    figura = models.ImageField(upload_to='producto', height_field=None, null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    status = models.BooleanField(default=True, choices=estado_choices )

    def __str__(self):
        return self.name
    
    def get_image(self):
        # si la imagen tiene datos
        if self.figura:
            return '{}{}'.format(MEDIA_URL, self.figura)
        else:
            return '{}{}'.format(STATIC_URL, 'img/Dado.png')

    
    def toJSON(self):
        # model_to_dict() se utiliza para convertir un objeto de modelo en un diccionario de Python.
        item = model_to_dict(self)
        item['cat'] = self.categoria_foreign.toJSON()
        # el or sive como "if" ya que lo que digo es que si no tiene self.get_image() colocame despues del "or"
        # item['figura'] = self.get_image() or '{}{}'.format(STATIC_URL, 'img/Dado.png')
        item['figura'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item
    
    class Meta:
        ordering = ['id']

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {
            'id': self.gender,
            'name': self.get_gender_display(),
        }
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d') #'%y-%m-%d'  %d-%m-%Y'
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names
    
    def toJSON(self):
        item = model_to_dict(self)
        print(item['cli'])
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item


    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']


