import json

from django.db.models.functions import Coalesce
from django.shortcuts import HttpResponse, get_object_or_404, render

from .forms import *
from .models import *


def create_product(product_info):
    ''' This creates a product '''
    form = ProductForm(product_info)
    if form.is_valid():
        form.save()
        return form.data
    else:
        return form.errors


def mass_create_product(loaded_data):
    ''' This creates multiple product '''
    return [create_product(data) for data in loaded_data]


def read_product(pk):
    ''' This give the information of a product '''
    product = Product.objects.get(pk=pk)

    # get field names of product
    fields = [i.name for i in product._meta.get_fields() if i.name !=
              'transaction']

    product_info = {}
    for i in fields:
        product_info[i] = getattr(product, i)

    # convert supplier object to json can read
    try:
        product_info['supplier'] = product_info['supplier'].serializable_value(
            'id')
    except:
        pass

    return product_info


def filter_products(q='all', limit=None, ordering={'order_by': 'name', 'order_type': None}):
    ''' Filter products query '''

    # if query value is None and all with no limit returns all product
    if q == 'all' and not limit:
        products = Product.objects.all()

    else:
        # if ordering and limit filter filter product with it's values
        if ordering and limit:
            if ordering.get('order_type') == 'descending':
                products = Product.objects.filter(name__icontains=q).order_by(
                    Coalesce(ordering.get('order_by'), ordering.get('order_by')
                             ).desc())[0:limit]
            else:
                products = Product.objects.filter(name__icontains=q).order_by(
                    ordering['order_by']
                )[0:limit]

        # if limit is not supplied but ordering is
        elif ordering and not limit:
            if ordering.get('order_type') == 'descending':
                products = Product.objects.filter(name__icontains=q).order_by(
                    Coalesce(ordering['order_by'], ordering['order_by']
                             ).desc())
            else:
                products = Product.objects.filter(name__icontains=q).order_by(
                    ordering['order_by']
                )
        # if ordering is None
        else:
            products = Product.objects.filter(name__icontains=q)[0:limit]

    return [{
        'name': product.name,
        'supplier': product.supplier_id,
        'stock': product.stock,
        'description': product.description
    } for product in products]


def update_product(product_data):
    product_id = product_data['productId']
    product_info = product_data['productInfo']

    product = Product.objects.get(pk=product_id)
    form = ProductForm(product_info, instance=product)
    if form.is_valid():
        form.save()
        return form.data
    else:
        return form.errors


def product_action(request, action):
    '''This function handles all the create, read, update, and delete on a product'''

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
            return HttpResponse('can\'t do that')
    else:
        loaded_data = json.loads(request.POST.get('json_data'))

        if action == 'create':
            # fields "name" required, "stock" required
            # "description", "barcode", "supplier" instance of Supplier model
            product_info_lenght = len(loaded_data)
            if request.POST.get('isMass'):
                # creates multiple product
                product_infos = loaded_data
                response_data = mass_create_product(product_infos)
            else:
                # create a single product
                product_info = loaded_data
                response_data = create_product(product_info)

            return HttpResponse(json.dumps(response_data))

        elif action == 'update':
            # fields "productId" required, "productInfo" required a dict object
            # ex. { "productInfo": {
            #       "name": "exName",           # required
            #       "stock": 100,               # required
            #       "barcode": 0291323,         # optional
            #       "supplier": 2,              # optional must be a supplier primary key
            #       "description": "exDesc"     # optional
            # }}
            response = update_product(loaded_data)

            return HttpResponse(json.dumps(response))

        elif action == 'delete':
            # fields required productId
            product_id = loaded_data['productId']
            product = get_object_or_404(Product.objects.all(), pk=product_id)
            product.delete()

            return HttpResponse(f'product with id {product_id} has been deleted')
        else:
            return HttpResponse('what are your doing bruh?')


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
