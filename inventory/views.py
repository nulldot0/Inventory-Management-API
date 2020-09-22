from django.shortcuts import render, HttpResponse
from .models import *
import json

def create_product(data):
    '''This function takes a data with dict as it's type'''

    # checks if a supplier is provided in the data given
    if data.get('supplier'):
        data['supplier'] = Supplier.objects.get(pk=data['supplier'])
        product = Product(**data)   
        data['supplier'] = data.get('supplier').serializable_value('name')
    else:
        product = Product(**data)

    product.save()

    # returns the details of product in dict type
    return {
        'product_name': product.name,
        'stock': product.stock,
        'supplier': data.get('supplier'),
        'description': data.get('description')
    }

def mass_create_product(datas):
    return [ create_product(data) for data in datas ]

def read_product(pk):
    product = Product.objects.get(pk=pk)
    
    if product.supplier:
        supplier = product.supplier.serializable_value('name')
    else:
        supplier = None

    return {
        'name': product.name,
        'stock': product.stock,
        'description': product.description,
        'supplier': supplier,
    }

def mass_read_product(pks):
    return [ read_product(pk) for pk in pks ]

def product_action(request, action):
    if request.method == 'GET':        
        if action == 'read':
            loaded_data = json.loads(request.GET.get('json_data'))

            if request.GET.get('isMass'):
                response_data = mass_read_product(loaded_data['productIds'])
            else:
                response_data = read_product(loaded_data['productId'])

            return HttpResponse(json.dumps(response_data))
    else:
        loaded_data = json.loads(request.POST.get('json_data'))

        if action == 'create':
            if request.POST.get('isMass'):
                response_data = mass_create_product(loaded_data)
            else:
                response_data = create_product(loaded_data)
            
            return HttpResponse(json.dumps(response_data))

        elif action == 'update':
            pass
        elif action == 'delete':
            pass
   
