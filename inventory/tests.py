from django.test import TestCase, Client
from . import models
from json import dumps, loads
import random
import string

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

    def testCreateProduct(self):
        client = Client()
        # create 10 product names
        product_names = [
                ''.join([
                    random.choices(string.ascii_letters)[0] for i in range(0, 10)
                ]) for i in range(0, 10)
            ]

        # creates the data to send as post request
        post_datas = [{
                'name': product_name,
                'stock': random.randint(1, 100),
                'supplier': random.randint(1, 10),
                'description': f'{product_name} description',
            } for product_name in product_names
        ]

        # sending the post data
        for post_data, product_name in zip(post_datas, product_names):
            response = client.post('/product/create/', {'json_data': dumps(post_data)})
            
            self.assertEqual(response.status_code, 200)

            # check if saved to database
            product_check = models.Product.objects.filter(**post_data).exists()
            self.assertEqual(product_check, True)

            # print(response.content)

    def testMassCreateProduct(self):
        client = Client()

        # create 10 product name
        product_names = [
                ''.join([
                    random.choices(string.ascii_letters)[0] for i in range(0, 10)
                ]) for i in range(0, 100)
            ]

        # create the post data
        post_data = [{
                'name': product_name,
                'stock': random.randint(1, 100),
                'supplier': random.randint(1, 10),
                'description': f'{product_name} description',
            } for product_name in product_names
        ]

        # send post request and save the response to response variable
        response = client.post('/product/create/', {'json_data': dumps(post_data), 'isMass': True})

        self.assertEqual(response.status_code, 200)

        # print(response.content)

    def testReadProduct(self):
        client = Client()
        
        filters = {
            'q': '',
            'limit': None,
            'ordering': {
                'order_by': 'id',
            },
        }

        # creates product ids to get
        productIds = [i for i in range(1, 101)]

        get_data = {
            # 'productId': random.choice(productIds),
            'filters': filters
        }

        # send get request
        response = client.get('/product/read/', {
                'json_data': dumps(get_data),
        })

        self.assertEqual(response.status_code, 200)

        print(response.content)
    
    def testUpdateProduct(self):
        prev_product = models.Product.objects.create(
            pk=1,
            name='Product1',
            stock=23,
            description='description1',
        )

        prev_name = prev_product.name

        client = Client()
        data = {
            'productId': 1,
            'name': 'Product2',
            'stock': 20,
            'supplier_id': 2,
            'description': 'description' 
        }

        res = client.post('/product/update/', {'json_data': dumps(data)})

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(prev_name, )
        print((str(res.content)))

    def testCreateSupplier(self):
        client = Client()

        response = client.post('/supplier/create/', {
            'json_data': dumps({
                'name': 'Supplier Test1',
                'email': 'jhpetalbo@gmail.com'
            })
        })

        self.assertEqual(response.status_code, 200)
        print(response.content)

    def testDeleteSupplier(self):
        client = Client()

        response = client.post('/supplier/delete/', dumps({
            'supplierId': 2
        }))
        self.assertEqual(response.status_code, 200)
        print(response.context)
