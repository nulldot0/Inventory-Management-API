import json

from django.shortcuts import HttpResponse, get_object_or_404, render

from .forms import *
from .models import *


def product_action(request, action):
    '''This function handles all the create, read, update, and delete on a product'''

    if request.method == 'GET':
        if action == 'read':
            loaded_data = json.loads(request.GET.get('jsonData'))
            response_data = read_model(loaded_data.get('productId'), Product, 'product')
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
                response_data = mass_create_model(
                    product_infos, Product, ProductForm)
            else:
                # create a single product
                product_info = loaded_data
                response_data = create_model(
                    product_info, Product, ProductForm)

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
            response_data = update_model(loaded_data.get(
                'productId'),  loaded_data.get('productInfo'), Product, ProductForm)

        elif action == 'delete':
            # fields required productId
            product_id = loaded_data.get('productId')
            response_data = delete_model(product_id, Product, 'product')
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
                response_data = read_model(supplier_id, Supplier, 'supplier')
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

            response_data = create_model(loaded_data, Supplier, SupplierForm)

        elif action == 'update':
            # updating a supplier
            response_data = update_model(loaded_data.get(
                'supplierId'), loaded_data.get('supplierInfo'), Supplier, SupplierForm)

        elif action == 'delete':
            # for deleting supplier
            # fields "supplierId"
            supplier_id = loaded_data.get('supplierId')

            response_data = delete_model(supplier_id, Supplier, 'supplier')
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


def transaction_action(request, action):
    if request.method == 'GET':
        loaded_data = json.loads(request.GET.get('jsonData'))
        if action == 'read':
            response_data = read_model(loaded_data.get('transactionId'), Transaction, 'transaction')
        else:
            response_data = {
                'isError': True,
                'errorInfo': 'action "{action}" not possible.'
            }
    else:
        loaded_data = json.loads(request.POST.get('jsonData'))

        if action == 'create':
            transaction_info = loaded_data
            response_data = create_model(
                transaction_info, Transaction, TransactionForm)
        elif action == 'update':
            transaction_id = loaded_data.get('transactionId')
            transaction_info = loaded_data.get('transactionInfo')
            if transaction_id:
                response_data = update_model(
                    transaction_id, transaction_info, Transaction, TransactionForm)
            else:
                response_data = {
                    'isError': True,
                    'errorInfo': 'Please provide a transaction Id'
                }
        elif action == 'delete':
            transaction_id = loaded_data.get('transactionId')
            response_data = delete_model(
                transaction_id, Transaction, 'transaction')
        else:
            response_data = {
                'isError': True,
                'errorInfo': f'please choose a valid action. ( create, read, update, delete )'
            }

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
    #   "query": "the query to search"   => optional, default is ''
    #   "query_by": "the field to query from the model" => default is "name"
    #   "query_limit": 100, => optional, must be an integer
    #   "order_by": "the field from the model"
    #    "order_type": "desc or ascn" => two choices only
    # }

    filters = json.loads(request.GET.get('jsonData'))
    # validate values with django forms
    if q_model == 'product':
        filter_form = QueryForm(filters)

        # queries the product objects
        response_data =  query_search(filter_form, Product, 'product')

    elif q_model == 'supplier':
        filter_form = QueryForm(filters)
        # queries the supplier objects
        response_data = query_search(filter_form, Supplier, 'supplier')

    elif q_model == 'transaction':
        filter_form = TransactionQueryForm(filters)
        # queries the transaction objects
        response_data =  query_search(filter_form, Transaction, 'transaction')
    else:
        # return an error response when models to query is invalid
        model_list = ['product', 'supplier', 'transaction']
        response_data = {
                    'isError': True,
                    'errorInfo': f'models to query does not exist. Please choose between ( {", ".join(model_list[:-1])}, and {model_list[-1]})'
                }
                
    return HttpResponse(
        json.dumps(
            {
                'responseData': response_data
            }
        )
    )

def query_search(filter_form, model_obj, model_name):
    if filter_form.is_valid():
        q = model_obj.objects.search(**filter_form.cleaned_data)
        if isinstance(q, dict):
            return q

        return [read_model(i.pk, model_obj, model_name) for i in q ]
    else:
        return {
            'isError': True,
            'errorInfo': filter_form.errors.as_json()
        }

def create_model(model_info, model_obj, model_form):
    # creates a new model
    form = model_form(model_info)

    if form.is_valid():
        form.save()
        return form.data
    else:
        return {
            'isError': True,
            'errorInfo': form.errors.as_json()
        }


def mass_create_model(loaded_data, model_obj, model_form):
    ''' This creates multiple model objects '''
    return [create_model(data, model_obj, model_form) for data in loaded_data]


def read_model(pk, obj, model_name):
    ''' This gives the information of a Model from Obj '''
    from datetime import datetime  # imported for checking fields with instance as datetime 
    model_tuple_check = (Product, Supplier) # used for for checking instances

    try:
        model_obj = obj.objects.filter(pk=pk).exists()
    except ValueError:
        return {
            'isError': True,
            'errorInfo': f'{model_name} id got an unidentified value.'
        }

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
                # checks if a instance of a models to for json serialization
                if isinstance(attribute_value, model_tuple_check):
                    model_info[i] = attribute_value.serializable_value('id')
                elif isinstance(attribute_value, datetime): # check if a datetime instance
                    model_info[i] = attribute_value.strftime('%Y-%m-%d %H:%M:%S:%f')
                else:
                    model_info[i] = getattr(model_obj, i)
            except:
                pass

        return model_info
    else:
        return {
            'isError': True,
            'errorInfo': f'{model_name} id does not exists'
        }


def update_model(model_id, model_info, model_obj, model_form):
    ''' This function updates an model '''
    if model_id:
        if not model_obj.objects.filter(pk=model_id).exists():
            return {
                'isError': True,
                'errorInfo': f'ID: {model_id} does not exists'
            }
        # changing info of model
        model_obj = model_obj.objects.get(pk=model_id)
        form = model_form(model_info, instance=model_obj)
        if form.is_valid():
            form.save()
            return form.data
        else:
            return {
                'isError': True,
                'errorInfo': form.errors.as_json()
            }
    else:
        return {
            'isError': True,
            'errorInfo': 'Please provide a id'
        }


def delete_model(model_id, model_obj, model_name):
    ''' This function deletes a model '''
    if model_id:
        try:
            if model_obj.objects.filter(pk=model_id).exists():
                model_obj.objects.get(pk=model_id)
                return f'{model_name} with id {model_id} deleted'
            else:
                return {
                    'isError': True,
                    'errorInfo': f'{model_name} with id {model_id} does not exists.'
                }
        except ValueError:
            return {
                'isError': True,
                'errorInfo': f'{model_name} got an unidentified value'
            }

    else:
        return {
            'isError': True,
            'errorInfo': f'Please provide a {model_name} id'
        }
