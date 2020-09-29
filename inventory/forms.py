from django import forms

from inventory.models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class QueryForm(forms.Form):
    query = forms.CharField(required=False)
    query_by = forms.CharField()
    query_limit = forms.IntegerField(initial=100, required=False)
    order_by = forms.CharField(empty_value='pk')
    order_type = forms.ChoiceField(choices=[
        ('desc', 'desc'),
        ('ascn', 'ascn')
    ], required=False)

class TransactionQueryForm(forms.Form):
    query_by = forms.CharField()
    query_by_suffix = forms.CharField(required=False, empty_value='contains')
    query = forms.CharField(required=False)
    query_limit = forms.IntegerField(initial=100, required=False)
    order_by = forms.CharField(empty_value='created_on')
    order_type = forms.ChoiceField(choices=[
        ('desc', 'desc'),
        ('ascn', 'ascn')
    ], required=False)