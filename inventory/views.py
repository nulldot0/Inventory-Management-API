from django.shortcuts import render, HttpResponse
from .models import *
import json
def product_action(request, action):
    if request.method != 'POST':        
        return HttpResponse('not a POST request.')
    
    if action == 'create':
        data = request.POST.get('json_data')
        data = json.loads(data)

        # filters the supplier if it exist or it is provided
        try:
            if data['supplier']:
                if Supplier.objects.filter(pk=data['supplier']).exists():
                    data['supplier'] = Supplier.objects.get(pk=data['supplier'])
                    supplier = data['supplier'].name
                else:
                    data['supplier'] = None
                    supplier = 'No supplier found'
        except:
            supplier = None

        product = Product(**data)
       
        product.save()

        response_details = {
                'product_name': product.name,
                'stock': product.stock,
                'supplier': supplier,
                'description': product.description
            }

        return HttpResponse(f'{json.dumps(response_details)}')

    elif action == 'read':
        pass
    elif action == 'update':
        pass
    elif action == 'delete':
        pass
   
