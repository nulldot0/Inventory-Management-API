import random
import string
from json import dumps, loads

from django.test import Client, TestCase

from inventory import forms, models


def setupModels(self):
    # create 10 supplier
    for i in range(0, 10):
        name_generator = ''.join([
            random.choices(string.ascii_letters)[0] for i in range(0, 10)
        ])
        models.Supplier.objects.create(name=name_generator)

    # create 100 product
    for i in range(0, 100):
        name_generator = ''.join([
            random.choices(string.ascii_letters)[0] for i in range(0, 10)
        ])

        models.Product.objects.create(
            name=name_generator,
            stock=random.randint(1, 100),
            supplier_id=random.randint(1, 10)
        )

class ViewSupplierCrudTest(TestCase):
    def testCreateSupplier(self):
        client = Client()

        response = client.post('/supplier/create/', {
            'json_data': dumps({
                'name': 'Supplier Test1',
                'email': 'jhpetalbo@gmail.com'
            })
        })

        self.assertEqual(response.status_code, 200)
        # print(response.content)

    def testDeleteSupplier(self):
        client = Client()
        supplier_id_to_delete = 2
        response = client.post('/supplier/delete/', {'json_data': {
            dumps({
                'supplierId': supplier_id_to_delete
            })
        }})

        total_supplier_created_on_setup = [
            i for i in range(1, len(models.Supplier.objects.all())+1)]
        # check if supplier id is supplied and in database
        if supplier_id_to_delete in total_supplier_created_on_setup:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 200)

        # check if Supplier is deleted from database or does not exist
        self.assertEqual(models.Supplier.objects.filter(
            pk=supplier_id_to_delete).exists(), False)

        # print(response.context)
