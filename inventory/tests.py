from django.test import TestCase, Client
from . import models

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
        models.Supplier.objects.create(name='test', pk=1)

    def testCreateProduct(self):
        client = Client()
        product_name = 'test1'

        data = {
            'name': product_name,
            'stock': 100,
            'description': 'epic',
            'supplier': 1
        }
        from json import dumps
        response = client.post('/product/create/', {'json_data': dumps(data)})
        
        self.assertEqual(response.status_code, 200)
        product = models.Product.objects.get(name=product_name)
        
        # prints response
        print(response.content)
        # check if product is same as given product_name
        self.assertEqual(product.name, product_name)

    def massProductCreate(self):
        pass