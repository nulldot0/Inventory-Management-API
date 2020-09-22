from django.test import TestCase, Client
from . import models
from json import dumps
import random


class ModelTest(TestCase):
    def setUp(self):
        models.Supplier.objects.create(name='Supplier Test')

    def testCreate(self):
        product = models.Product.objects.create(name='Product', stock=100)
        
        add_stock = 100
        initial_stock = product.stock
        transaction = models.Transaction(product=product, stock=add_stock).save()

        self.assertEqual(product.stock, (add_stock+initial_stock))

class ViewTest(TestCase):
    def setUp(self):
        models.Supplier.objects.create(name='supplier1', pk=1)
        models.Supplier.objects.create(name='supplier2', pk=2)



    def testCreateProduct(self):
        client = Client()
        product_names = ['test1', 'test2', 'test3', 'test4', 'test5']
        stocks = [100, 20, 30, 10, 20]
        suppliers = [1, 2, 1, 2, 1]
        descriptions = ['description', 'test', '', '', 'test2']
        data = []
        [
            data.append({
                'name': prod_name,
                'stock': stock,
                'supplier': supplier,
                'description': description,
            }) for prod_name, stock, supplier, description in zip(product_names, stocks, suppliers, descriptions)
        ]

        for i, j in zip(data, product_names):
            response = client.post('/product/create/', {'json_data': dumps(i)})
            
            self.assertEqual(response.status_code, 200)
           
            product = models.Product.objects.get(name=j)
 
            # prints response
            print(response.content)
            # check if product is same as given product_name
            self.assertEqual(product.name, j)

    def testMassCreateProduct(self):
        client = Client()
        product_names = ['test1', 'test2', 'test3', 'test4', 'test5']
        stocks = [100, 20, 30, 10, 20]
        suppliers = [1, 2, 1, 2, 1]
        descriptions = ['description', 'test', '', '', 'test2']
        data = []
        # 
        [
            data.append({
                'name': prod_name,
                'stock': stock,
                'supplier': supplier,
                'description': description,
            }) for prod_name, stock, supplier, description in zip(product_names, stocks, suppliers, descriptions)
        ]

        response = client.post('/product/create/', {'json_data': dumps(data), 'isMass': True})
        self.assertEqual(len(models.Product.objects.all()), 5)

        print(response.content)

    def testReadProduct(self):
        pks = [x for x in range(1, 10)]
        for i in pks:
            models.Product.objects.create(
                pk=i,
                name=f'Product {i}', 
                stock=random.randint(1, 100),
                description=f'description {i}',
                supplier=models.Supplier.objects.get(pk=random.choice([1,2]))
            )

        client = Client()

        data = {
            'productId': random.choice(pks)
        }
        res = client.get('/product/read/', {
                'json_data': dumps(data)
            })

        # for mass read
        data = {
            'productIds': pks
        }
        res = client.get('/product/read/', {
                'json_data': dumps(data), 'isMass': True
            })
        
        print(res.content)

        self.assertEqual(res.status_code, 200)

        print(res.content)
