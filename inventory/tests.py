import random
import string
from json import dumps, loads

from django.test import Client, TestCase

from inventory import forms, models

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

        # creates product ids to get
        productIds = [i for i in range(1, 101)]

        # read info of a product
        get_data = {
            'productId': random.choice(productIds)
        }

        # send request
        response = client.get('/product/read/', {
                'json_data': dumps(get_data),
        })

        self.assertEqual(response.status_code, 200)
        
        query = ''
        limit = None
        
        # products info filter data
        get_data = {
            'filters': {
                'q': query,
                'limit': limit,
                'ordering': {
                    'order_by': 'name',
                    'order_type': 'descending'
                }
            }
        }

        # send get request
        response = client.get('/product/read/', {
                'json_data': dumps(get_data),
        })

        self.assertEqual(response.status_code, 200)

        # check if products count matches limit
        if limit:
            self.assertEqual(len(loads(response.content)), limit)
        
        # check if product models length is same with response data
        if not query:
            self.assertEqual(len(loads(response.content)), len(models.Product.objects.all()))

        print(response.content)
    
    def testUpdateProduct(self):
        random_pk = random.randint(0, 100)
        prev_product = models.Product.objects.get(pk=random_pk)

        client = Client()
        # data to send
        data = {
            'productId': random_pk,                     # product id to update
            'productInfo': {                            # product information
                'name': 'updated name',                 # "name" required
                'stock': 100,                           # "stock" required
                'description': 'updated description',   # "description" optional
                'barcode': 20395343,                    # "barcode" optional
                'supplier': 1,                          # "supplier" optional
            }
        }

        response = client.post('/product/update/', {'json_data': dumps(data)})
        
        self.assertEqual(response.status_code, 200)

        # check if product is updated
        self.assertEqual(models.Product.objects.filter(**data['productInfo']).exists(), True)

        # print(response.content)

    def testDeleteProduct(self):
        client = Client()

        response = client.post('/product/delete/', {'json_data': dumps({'productId': 2 })})

        self.assertEqual(response.status_code, 200)

        print(response.content)

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
