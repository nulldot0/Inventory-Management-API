
import random
import string
from json import dumps, loads

from django.test import Client, TestCase

from . import forms, models


def send_request(data, url, method='POST'):
    ''' sending data to servier'''
    client = Client()

    if method == 'POST':
        response = client.post(url, {
            'jsonData': dumps(data)
        })
    else:
        response = client.get(url, {
            'jsonData': dumps(data)
        })

    return response


class ProductView(TestCase):
    def setUp(self):
        # create 10 supplier
        for i in range(0, 10):
            name_generator = ''.join([
                random.choices(string.ascii_letters)[0] for i in range(0, 10)
            ])
            models.Supplier.objects.create(name=name_generator)

        # create 100 product
        for i in range(0, 50):

            name_generator = ''.join([
                random.choice(string.ascii_letters) for i in range(0, 10)
            ])

            barcode_generator = ''.join([
                random.choice(string.digits) for i in range(0, 12)
            ])

            # create product with supplier and description
            models.Product.objects.create(
                name=name_generator,
                stock=random.randint(1, 100),
                barcode=barcode_generator,
                supplier_id=random.randint(1, 10),
                description=f'{name_generator} description'
            )

            # create product without supplier
            models.Product.objects.create(
                name=name_generator,
                stock=random.randint(1, 100),
            )

    def testQuery(self):
        ''' Testing for querying a product '''
        client = Client()

        response = client.get('/query/product/', {
            'jsonData': dumps(
                {
                    'filters': {                                # creating the query data
                        'query': '10',
                        'query_by': 'test',
                        'query_limit': 100,
                        'order_by': 'id',
                        'order_type': 'ascn'
                    }
                }
            )
        })

        response_data = loads(response.content)
        # [print(i) for i in response_data['responseData']]

    def testCreate(self):
        ''' testing product create'''
        client = Client()

        invalid_product_name = random.choice([None, '', 1])
        invalid_stock = random.choice([random.choice(range(-100, 0)), None])
        invalid_barcode = ''.join(
            [random.choice(string.ascii_letters) for i in range(0, 101)])
        invalid_supplier = ''

        post_data_required_field_not_supplied = {
            'barcode': 'test'
        }

        response = client.post(
            '/product/create/', {
                'jsonData': dumps(post_data_required_field_not_supplied)
            })

        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content)['responseData']
        # check if response has errors
        self.assertTrue(response_data.get('isError'))

        # creates the data to send as post request with invalid values in fields
        post_data_invalid = {
            'name': invalid_product_name,
            'stock': invalid_stock,
            'supplier': invalid_supplier,
            'barcode': invalid_barcode,
            'description': f'{invalid_product_name} description',
        }

        # sending the post data with invalid values
        response = client.post(
            '/product/create/', {
                'jsonData': dumps(post_data_invalid)
            })

        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content)['responseData']
        # check if response has errors
        self.assertTrue(response_data.get('isError'))

        # # print(response_data)

        # creates the data to send as post request with valid values in fields
        valid_product_name = 'Product Valid'
        valid_barcode = '239123'
        valid_supplier = 10
        valid_stock = 100,

        post_data_valid = {
            'name': valid_product_name,
            'stock': valid_barcode,
            'barcode': valid_barcode,
            'description': f'{valid_product_name} description',
            'supplier': valid_supplier
        }

        supplier = (models.Supplier.objects.get(pk=valid_supplier))
        # sending the post data with valid values
        response = client.post(
            '/product/create/', {
                'jsonData': dumps(post_data_valid)
            }
        )

        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content)['responseData']
        # check if response has no errors
        self.assertIsNone(response_data.get('isError'))

        # print(response_data)

    def testMassCreate(self):

        # create 10 product name
        product_names = [
            ''.join([
                    random.choices(string.ascii_letters)[0] for i in range(0, 10)
                    ]) for i in range(0, 100)
        ]

        # create the post data
        post_data = [
            {
                'name': product_name,
                'stock': random.randint(1, 100),
                'supplier': random.randint(1, 10),
                'description': f'{product_name} description',
            } for product_name in product_names
        ]

        # send post request and save the response to response variable
        client = Client()
        response = client.post(
            '/product/create/', {
                'jsonData': dumps(post_data),
                'isMass': True
            }
        )

        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content)['responseData']
        # print(response_data)

    def testRead(self):
        # creates product ids to get
        productIds = [i for i in range(1, 101)]

        # read info of a product
        get_data = {
            'productId': 101
        }

        # create a product with no supplier
        models.Product(**{
            'pk': 101,
            'name': 'test read product',
            'description': 'description',
        }).save()

        # send request
        client = Client()
        response = client.get('/product/read/', {
            'jsonData': dumps(get_data),
        })

        self.assertEqual(response.status_code, 200)

        # print(response.content)

    def testUpdate(self):
        random_pk = random.randint(0, 100)
        prev_product = models.Product.objects.get(pk=random_pk)

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

        # sending the request
        client = Client()
        response = client.post('/product/update/', {'jsonData': dumps(data)})

        self.assertEqual(response.status_code, 200)

        # check if product is updated
        self.assertEqual(models.Product.objects.filter(
            **data['productInfo']).exists(), True)

        # print(response.content)

    def testDelete(self):

        # sending the request
        client = Client()
        response = client.post(
            '/product/delete/', {'jsonData': dumps({'productId': 2})})

        self.assertEqual(response.status_code, 200)

        # print(response.content)

    def testActionUnidentified(self):
        # sending the request
        client = Client()
        response = client.post(
            '/product/s/', {'jsonData': dumps({'productId': 2})})

        self.assertEqual(response.status_code, 200)

        # print(response.content)


class SupplierView(TestCase):
    def setUp(self):
        # create 10 suppliers
        supplier_names = [
            ''.join(
                random.choice(string.ascii_letters) for i in range(10)
            ) for i in range(10)
        ]

        [models.Supplier.objects.create(name=i) for i in supplier_names]

    def testCreate(self):
        ''' testing supplier create'''
        # suppplier valid info to send
        supplier_valid_info = {
            'name': 'Supplier Valid Name',
            'mobile_number': 91204223,
            'email': 'jhpetalbo@gmail.com',
            'address': 'brgy. string, python'
        }

        response = send_request(supplier_valid_info, '/supplier/create/')

        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # self.assertEqual(
        # len(models.Supplier.objects.filter(**supplier_valid_info)), 1)

        # print(response_data)

        # supplier invalid info to send
        supplier_invalid_info = {
            'mobile': 'a string',
            'email': 'not an email',
            'address': 123,
        }

        response = send_request(supplier_invalid_info, '/supplier/create/')

        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content).get('responseData')
        # check if response has errors
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

    def testRead(self):
        ''' testing supplier read '''

        valid_supplier_id = {
            'supplierId': 10
        }

        response = send_request(valid_supplier_id, '/supplier/read/', 'GET')

        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')

        # print(response_data)

        # supplier id that doesn't exist
        does_not_exist_supplier_id = {
            'supplierId': 101
        }

        response = send_request(
            does_not_exist_supplier_id, '/supplier/read/', 'GET')

        # checks response error
        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content).get('responseData')
        # check if error
        self.assertTrue(response_data['isError'])

        # print(response.content)

    def testQuery(self):
        ''' testing supplier query '''
        filters = {
            'query': 't',
            'query_by': 'name',
            'query_limit': 2,
            'order_by': 'name',
            'order_type': 'desc'
        }

        response = send_request(filters, '/query/supplier/', 'GET')
        self.assertEqual(response.status_code, 200)

        # print(response.content)

    def testDelete(self):
        ''' testing supplier delete '''
        url = '/supplier/delete/'

        # sending valid data
        valid_data = {
            'supplierId': 1
        }

        response = send_request(valid_data, url)

        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content).get('responseData')

        # print(response_data)

        # sending invalid data
        invalid_data = {
            'supplierId': 100
        }
        
        response = send_request(invalid_data, url)
        response_data = loads(response.content).get('responseData')
        
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

        # sending invalid data
        invalid_data = {
            'id': 100
        }
        
        response = send_request(invalid_data, url)
        response_data = loads(response.content).get('responseData')
        
        self.assertTrue(response_data.get('isError'))

        # print(response_data)


    def testUpdate(self):
        url = '/supplier/update/'

        previous_supplier = models.Supplier.objects.get(pk=1)
        
        # sending valid supplier info
        valid_supplier_info = {
            'supplierId': 1,
            'name': 'Supplier Name updated',
            'email': 'supplieremail@updated.com',
            'address': 'supplier updated address'
        }

        response = send_request(valid_supplier_info, url)
        
        # checking error
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertNotEqual(previous_supplier.name, valid_supplier_info['name'])
        print(response_data)

        # sending invalid supplier info
        invalid_supplier_info = {
            'n': 'test',
            'test', 123,
            'tes2', None
        }
        
        # checking error
        response = send_request(invalid_supplier_info, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError')) 
        print(response_data)           




