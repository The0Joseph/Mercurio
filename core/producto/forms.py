from datetime import datetime
from django import forms
from core.producto.models import producto, categoria, Client, DetSale, Sale

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        
        self.fields['name'].widget.attrs.update({'class':'form-control border-0', 'aria-describedby': 'button-addon3'})
        self.fields['figura'].widget.attrs.update({'class':'form-control border-0'})

        # for form in self.visible_fields:
        #     form.field.attrs['class'] = 'form-control'

    class Meta:
        model = producto
        # Las columnas a mandar
        fields = '__all__'
        # Excluir formularios
        exclude = ['status']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre de producto',
                'title': 'Ingrese un nombre de una producto',
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
                
        except Exception as e:
            data['error'] = str(e)
        return data
    
class CategoriaFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        self.fields['name'].widget.attrs.update({'class':'form-control border-0', 'aria-describedby': 'button-addon3'})

    class Meta:
        model = categoria
        fields = '__all__'
        exclude = ['status','user_creation','user_update']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese una Categoria',
                'title': 'Ingrese un nombre para una Categoria'
            }),

        }
    
    def save(self, commit= True):
        data = {}
        form = super()

        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client   
        fields = '__all__'
        widgets = {
            'names' : forms.TextInput(attrs={
                'placeholder': 'Nombre del cliente',
                'title': 'Ingrese un nombre del cliente'
            }),
            'date_birthday': forms.DateInput(format='%Y-%m-%d', attrs={ #'%Y-%m-%d'  DD-MM-YYYY
                'value': datetime.now().strftime('%Y-%m-%d') #'%Y-%m-%d'
            }),
            'gender': forms.Select()
        }

    def save(self, commit= True):
        data = {}
        form = super()

        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(forms.Form):
    cate = forms.ModelChoiceField(queryset=categoria.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2'
    }))
    prod = forms.ModelChoiceField(queryset=producto.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2'
    }))

    # search = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese algo que desee buscar'
    # }))
    search =  forms.ModelChoiceField(queryset=categoria.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2'
    }))


class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        # self.fields['cli'].widget.attrs.update({'class':'form-control select2'})

    class Meta:
        model = Sale
        fields = '__all__'
        # exclude = ['user_creation','user_update']

        widgets = {
            'cli':forms.Select(attrs={
                'class': 'select2'
            }),
            'date_joined': forms.DateInput(format='%Y-%m-%d',attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True
            }),

            'iva':forms.TextInput(),

            'total': forms.TextInput(attrs={
                'readonly': True
            })
            

        }
    
        
