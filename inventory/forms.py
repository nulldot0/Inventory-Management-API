from django.forms import ModelForm
from inventory.models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
