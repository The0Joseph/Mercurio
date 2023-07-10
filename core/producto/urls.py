from django.urls import path
# from core.producto.views import Tierra
from core.producto.views.producto.views import *
from core.producto.views.categoria.views import *
from core.producto.views.cliente.views import *
from core.producto.views.sale.views import *
from core.producto.views.test.views import *


app_name = 'producto'

urlpatterns = [
    path('producto/list', TierraListView.as_view(), name="Producto_list"),
    path('producto/add/', TierraCreateView.as_view(), name="Producto_add"),
    path('producto/edit/<int:pk>/', TierraUpdateView.as_view(), name="Producto_edit"),
    path('producto/delete/<int:pk>/', TierraDeleteView.as_view(), name="Producto_delete"),

    # Categorias

    path('categoria/list', CategoriaListView.as_view(), name="Categoria_list"),
    path('categoria/add', CategoriaCreateView.as_view(), name="Categoria_create"),
    path('categoria/edit/<int:pk>/', CategoriaUpdateView.as_view(), name="Categoria_edit"),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name="Categoria_delete"),
    
    # CLient
    path('cliente/', ClientView.as_view(), name="cliente"),

    # test
    path('test/', TestListView.as_view(), name="test"),
    
    # Venta
    path('venta/list', SaleListView.as_view(), name="Venta_list"),
    path('venta/create', SaleCreateView.as_view(), name="Venta_create"),
    path('venta/edit/<int:pk>/', SaleEditView.as_view(), name="Venta_edit"),
    
    # PDFs
    path('venta/invoice/pdf/<int:pk>/', SaleInvoicePDFview.as_view(), name="Venta_invoice_pdf"),



]
