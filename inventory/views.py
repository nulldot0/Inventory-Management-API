import json
from django.shortcuts import render, HttpResponse
from django.db.models.functions import Coalesce
from . models import *
from .forms import *

def create_product(loaded_data):
    form = ProductForm(loaded_data)
    if form.is_valid():
        form.save()
        return form.data
    else:
        return form.errors

def mass_create_product(loaded_data):
    return [ create_product(data) for data in loaded_data ]

def read_product(pk):
    product = Product.objects.get(pk=pk)

    # get field names of product
    fields = [i.name for i in product._meta.get_fields() if i.name != 'transaction']

    product_info = {}
    for i in fields:
        product_info[i] = getattr(product, i)
    
    # convert supplier object to json can read
    try:
        product_info['supplier'] = product_info['supplier'].serializable_value('id')
    except:
        pass

    return product_info

def filter_products(q='all', limit=None, ordering={'order_by': 'name', 'order_type': None}):
    ''' Filter products query '''

    if q == 'all' and not limit:
        products = Product.objects.all()
    else:
        if ordering and limit:
            if ordering.get('order_type') == 'descending':
                    products = Product.objects.filter(name__icontains=q).order_by(
                        Coalesce(ordering.get('order_by')
                    ).desc())[0:limit]
            else:
                products = Product.objects.filter(name__icontains=q).order_by(
                        ordering['order_by']
                    )
        elif ordering and not limit:
            if ordering.get('order_type') == 'descending':
                    products = Product.objects.filter(name__icontains=q).order_by(
                        Coalesce(ordering['order_by']
                    ).desc())
            else:
                products = Product.objects.filter(name__icontains=q).order_by(
                        ordering['order_by']
                    )
        else:
            products = Product.objects.filter(name__icontains=q)[0:limit]

    return [{
        'name': product.name,
        'supplier': product.supplier_id,
        'stock': product.stock,
        'description': product.description
    } for product in products ]

def update_product(**kwargs):
    product = Product.objects.get(pk=kwargs['productId'])
    del(kwargs['productId'])
    return product

def product_action(request, action):
    if request.method == 'GET':        
        if action == 'read':
            loaded_data = json.loads(request.GET.get('json_data'))

            if not loaded_data.get('productId'):
                # field "filters" a json object
                #    ex. filters = {
                #       "q": "test"                      # default is "all", product query name,
                #        "limit": 20                     # default is "None"
                #        "ordering": {
                #         "order_by": "id",             # default is "name"
                #         "order_type": "descending"    # default is "None"
                #     }
                # }
                
                response_data = filter_products(**loaded_data['filters'])
            else:
                # fields "productId" required
                response_data = read_product(loaded_data['productId'])
            
            return HttpResponse(json.dumps(response_data))
    else:
        loaded_data = json.loads(request.POST.get('json_data'))

        if action == 'create':
            # fields "name" required, "stock" required
            # "description", "barcode", "supplier" instance of Supplier
             
            if request.POST.get('isMass'):
                response_data = mass_create_product(loaded_data)
            else:
                response_data = create_product(loaded_data)
                
            return HttpResponse(json.dumps(response_data))        

        elif action == 'update':
            product = update_product(**loaded_data)

            return HttpResponse(json.dumps({
                'name': product.name,
                'stock': product.stock,
                'description': product.description,
                'supplier': product.supplier.serializable_value('name'),
            }))

        elif action == 'delete':
            pass
   

def create_supplier(supplier_info):
    # creates a new supplier
    supplier = SupplierForm(supplier_info)
    if supplier.is_valid():
        supplier.save()

        return supplier.data
    else:
        return supplier.errors

def supplier_action(request, action):
    # CREATE, READ, UPDATE, and DELETE supplier
    if request.method == 'GET':
        if action == 'read':
            pass
    else:
        loaded_data = json.loads(request.POST.get('json_data'))
        
        if action == 'create':
            # For creating a new supplier 
            # fields "name" required, "mobile_number", "email", "address"
            
            response = create_supplier(loaded_data)
            return HttpResponse(json.dumps(response))

        elif action == 'update':
            pass
        else:
            # for deleting supplier
            # fields "supplierId"
            supplier_id = loaded_data['supplierId']
            print(supplier_id)
            if Supplier.objects.filter(pk=supplier_id).exists():
                Supplier.objects.get(pk=supplier_id).delete()
                message = f'supplier with id {supplier_id} deleted'
            else:
                message = f'supplier with id {supplier_id} does not exists.'

            return HttpResponse(json.dumps({'message': message}))



