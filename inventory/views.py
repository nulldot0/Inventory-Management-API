import json

from django.shortcuts import HttpResponse, get_object_or_404, render

from .forms import *
from .models import *


def product_action(request, action):
    '''This function handles all the create, read, update, and delete on a product'''

    if request.method == 'GET':
        if action == 'read':
            loaded_data = json.loads(request.GET.get('jsonData'))
            if loaded_data.get('productId'):
                # fields "productId" required
                response_data = read_model(loaded_data['productId'], Product)
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
        loaded_data = json.loads(request.POST.get('jsonData'))

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
    ''' CREATE, READ, UPDATE, and DELETE supplier '''
    if request.method == 'GET':
        # this action read information of a supplier
        if action == 'read':
            loaded_data = json.loads(request.GET.get('jsonData'))

            supplier_id = loaded_data.get('supplierId')

            if supplier_id:
                response_data = read_model(supplier_id, Supplier)
            else:
                response_data = {
                        'isError': True,
                        'errorInfo': 'Please provide a supplier id'
                    }
        else:
            response_data = {
                'isError': True,
                'errorInfo': f'action {action} possible'
            }

    else:
        loaded_data = json.loads(request.POST.get('jsonData'))

        if action == 'create':
            # For creating a new supplier
            # fields 
            # "name" required 
            # "mobile_number" optional
            # "email" optional
            # "address" optional

            response_data = create_supplier(loaded_data)

        elif action == 'update':
            pass
        elif action == 'delete':
            # for deleting supplier
            # fields "supplierId"
            supplier_id = loaded_data.get('supplierId')
            if Supplier.objects.filter(pk=supplier_id).exists():
                Supplier.objects.get(pk=supplier_id).delete()
                response_data = f'supplier with id {supplier_id} deleted'
            else:
                if supplier_id == None:
                    errorInfo = 'please provide an "supplierId" to delete'
                else:
                    errorInfo = f'supplier with id {supplier_id} does not exists.'

                response_data = {
                    'isError': True,
                    'errorInfo': errorInfo
                }
        else:
            # return this message if action is invalid
            response_data = 'choose a valid action. (create, delete, read, and update)'

    return HttpResponse(
        json.dumps(
            {
                'responseData': response_data
            }
        )

    )


def query(request, q_model):
    ''' This function handles the query of the models '''

    # JSON OBJECT TO SEND
    # filters = {
    #   "query": "the query to search"   => optional, default is all
    #   "query_by": "the field to query from the model" => default is "name"
    #   "query_limit": 100, => optional, must be an integer
    #   "order_by": "the field from the model"
    #    "order_type": "desc or ascn" => two choices only
    # }

    query_info = json.loads(request.GET.get('jsonData'))
    # loads the filter
    filters = query_info.get('filters')
    # validate values with django forms
    filter_form = QueryForm(filters)
    if q_model == 'product':
        if filter_form.is_valid():
            # search query
            q = Product.objects.search(**filter_form.cleaned_data)

            # get fields and it's values
            product_infos = [read_model(i.pk, Product) for i in q]
        else:
            q = Product.objects.all()
            product_infos = [read_model(i.pk, Product) for i in q]

        return HttpResponse(
            json.dumps(
                {
                    'responseData': product_infos
                }
            )
        )

    elif q_model == 'supplier':
        if filter_form.is_valid():
            # queries the supplier objects
            q = Supplier.objects.search(**filter_form.cleaned_data)

            # gets the supplier info
            supplier_infos = [read_model(i.pk, Supplier) for i in q]

            return HttpResponse(
                json.dumps(
                    {
                        'responseData': supplier_infos
                    }
                )
            )
        else:
            # if query forms has errors
            return HttpResponse(
                json.dumps(
                    {
                        'isError': True,
                        'errorInfo': filter_form.errors.as_json()
                    }
                )
            )
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


def read_model(pk, obj):
    ''' This gives the information of a Model from Obj '''

    model_obj = obj.objects.filter(pk=pk).exists()

    if model_obj:
        model_obj = obj.objects.get(pk=pk)
        # get the models fields
        fields = [
            i.name for i in model_obj._meta.get_fields()
        ]

        model_info = {}

        # Looping through fields of model to get its value to save in model_info
        for i in fields:
            try:
                attribute_value = getattr(model_obj, i)
                # checks if a instance of a models to serialize the id
                if (isinstance(attribute_value, (Product, Supplier))):
                    model_info[i] = attribute_value.serializable_value('id')
                else:
                    model_info[i] = getattr(model_obj, i)
            except:
                pass

        return model_info
    else:
        return {
            'isError': True,
            'errorInfo': 'Id does not exists'
        }


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
