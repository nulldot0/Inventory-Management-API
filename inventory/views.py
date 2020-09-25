import json

from django.shortcuts import HttpResponse, get_object_or_404, render

from .forms import *
from .models import *


def product_action(request, action):
    '''This function handles all the create, read, update, and delete on a product'''

    if request.method == 'GET':
        if action == 'read':
            loaded_data = json.loads(request.GET.get('json_data'))
            if loaded_data.get('productId'):
                # fields "productId" required
                response_data = read_product(loaded_data['productId'])
            else:
                response_data = {
                    'isError': True,
                    'errorInfo': 'Please provide a product ID'
                }
        else:
            response_data = {
                'isError': True,
                'errorInfo': f'action {action} is not possible'
            }
    else:
        loaded_data = json.loads(request.POST.get('json_data'))

        if action == 'create':
            # fields "name" required, "stock" required
            # "description", "barcode", "supplier"
            product_info_lenght = len(loaded_data)
            if request.POST.get('isMass'):
                # creates multiple product
                product_infos = loaded_data
                response_data = mass_create_product(product_infos)
            else:
                # create a single product
                product_info = loaded_data
                response_data = create_product(product_info)

        elif action == 'update':
            #  JSON OBJECT TO SEND
            # fields "productId" required, "productInfo" required a dict object
            # ex. { "productInfo": {
            #       "name": "exName",           # required
            #       "stock": 100,               # required
            #       "barcode": 0291323,         # optional
            #       "supplier": 2,              # optional must be a supplier primary key
            #       "description": "exDesc"     # optional
            # }}
            response_data = update_product(loaded_data)

        elif action == 'delete':
            # fields required productId
            product_id = loaded_data['productId']
            product = get_object_or_404(Product.objects.all(), pk=product_id)
            product.delete()
            response_data = f'product with id {product_id} has been deleted'
        else:
            response_data = {
                'isError': True,
                'errorInfo': f'action "{action}" is not possible'
            }

    return HttpResponse(json.dumps({'responseData': response_data}))


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

            response_data = create_supplier(loaded_data)
            # return HttpResponse(json.dumps(response))

        elif action == 'update':
            pass
        else:
            # for deleting supplier
            # fields "supplierId"
            supplier_id = loaded_data['supplierId']
            if Supplier.objects.filter(pk=supplier_id).exists():
                Supplier.objects.get(pk=supplier_id).delete()
                message = f'supplier with id {supplier_id} deleted'
            else:
                message = f'supplier with id {supplier_id} does not exists.'

            return HttpResponse(json.dumps({'message': message}))


def query(request, q_model):
    ''' This function handles the query of the models '''
    
    # JSON OBJECT TO SEND 
    # filters = {
    #   "query": "the query to search"   => optional, default is all
    #   "query_by": "the field to query from the Product model" => default is "name"
    #   "query_limit": 100, => optional, must be an integer
    #   "order_by": "the field from the Product model"
    #    "order_type": "desc or ascn" => two choices only
    # }

    query_info = json.loads(request.GET.get('json_data'))
    # loads the filter
    filters = query_info.get('filters')

    if q_model == 'product':
        # validate values with django forms
        filter_form = QueryProductForm(filters)

        if filter_form.is_valid():
            # search query
            q = Product.objects.search(**filter_form.cleaned_data)

            # get fields and it's values
            product_infos = [read_product(i.pk) for i in q]
        else:
            q = Product.objects.all()
            product_infos = [read_product(i.pk) for i in q]

        return HttpResponse(
            json.dumps(
                {
                    'responseData': product_infos
                }
            )
        )

    elif q_model == 'supplier':
        pass
    elif q_model == 'transaction':
        pass
    else:
        # return an error response when models to query is invalid
        return HttpResponse(
            json.dumps(
                {
                    'isError': True,
                    'errorInfo': 'models to query does not exist.'
                }
            )
        )


def create_supplier(supplier_info):
    # creates a new supplier
    supplier = SupplierForm(supplier_info)
    if supplier.is_valid():
        supplier.save()

        return supplier.data
    else:
        return {
            'isError': True,
            'errorInfo': supplier.errors.as_json()
        }


def create_product(product_info):
    ''' This creates a product '''
    form = ProductForm(product_info)
    if form.is_valid():
        form.save()
        return form.data
    else:
        return {
            'isError': True,
            'errorInfo': form.errors.as_json()
        }


def mass_create_product(loaded_data):
    ''' This creates multiple product '''
    return [create_product(data) for data in loaded_data]


def read_product(pk):
    ''' This give the information of a product '''
    product = get_object_or_404(Product, pk=pk)

    # get field names of product
    fields = [
        i.name for i in product._meta.get_fields() if i.name != 'transaction'
    ]

    product_info = {}
    for i in fields:
        product_info[i] = getattr(product, i)

    # convert supplier object to json can read
    try:
        product_info['supplier'] = product_info['supplier'].serializable_value(
            'id'
        )
    except:
        pass

    return product_info


def update_product(product_data):
    product_id = product_data['productId']
    product_info = product_data['productInfo']

    product = Product.objects.get(pk=product_id)
    form = ProductForm(product_info, instance=product)
    if form.is_valid():
        form.save()
        return form.data
    else:
        return form.errors.as_json()
