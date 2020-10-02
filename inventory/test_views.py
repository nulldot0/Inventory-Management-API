
import random
import string
from json import dumps, loads

from django.test import Client, TestCase

from . import forms, models


def send_request(data, url, method='POST'):
    ''' sending data to server '''
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

    def testCreate(self):
        ''' Testing product create'''
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
        ''' Testing product mass create '''
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
        ''' Testing product read '''
        url = '/product/read/'
        # read info of a product
        valid_product_id = {
            'productId': 22
        }

        response = send_request(valid_product_id, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')

        # print(response_data)

        invalid_product_id = {
            'productId': 200
            # 'productId': None
        }

        response = send_request(invalid_product_id, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

    def testUpdate(self):
        ''' Testing product update. '''
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
        self.assertTrue(models.Product.objects.filter(
            **data['productInfo']).exists())

        # print(response.content)

    def testDelete(self):
        ''' Testing product delete '''
        url = '/product/delete/'

        # sending request with valid product id
        valid_product_id = {
            'productId': 2
        }
        response = send_request(valid_product_id, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')

        # print(response_data)
        # sending request with invalid product id
        invalid_product_id = {
            'productId': 'te'
        }

        response = send_request(invalid_product_id, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

    def testActionUnidentified(self):
        ''' Testing product action unidentified '''
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
        ''' Testing supplier create'''
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
        ''' Testing supplier read '''

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

    def testDelete(self):
        ''' Testing supplier delete '''
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
        ''' Testing supplier update '''
        url = '/supplier/update/'

        previous_supplier = models.Supplier.objects.get(pk=1)

        # sending valid supplier info
        valid_supplier_info = {
            'supplierId': 1,
            'supplierInfo': {
                'name': 'Supplier Name updated',
                'email': 'supplieremail@updated.com',
                'address': 'supplier updated address'
            }
        }

        response = send_request(valid_supplier_info, url)

        # checking error
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertNotEqual(
            previous_supplier.name,
            valid_supplier_info['supplierInfo']['name']
        )

        # print(response_data)

        # sending invalid supplier info
        invalid_supplier_info = {
            'n': 'test',
            'test': 123,
            'tes2': None
        }

        # checking error
        response = send_request(invalid_supplier_info, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))

        # print(response_data)


class TransactionView(TestCase):
    def setUp(self):
        from datetime import datetime
        # creating 100 transactions
        product = models.Product.objects.create(
            pk=1, name='test product', stock=5000)
        models.Product.objects.create(
            pk=2, name='test product 1', stock=3000)

        for i in range(100):
            models.Transaction(
                product=product, stock=100, note='test note').save()

    def testCreate(self):
        ''' Testing transaction create '''
        url = '/transaction/create/'

        # sending request with valid transaction info
        valid_transaction_info = {
            'id': 101,
            'product': 1,
            'stock': 100,
            'note': 'created test note'
        }

        response = send_request(valid_transaction_info, url)
        self.assertEqual(response.status_code, 200)

        response_data = loads(response.content).get('responseData')
        # check if transaction is saved in database
        self.assertTrue(models.Transaction.objects.filter(pk=101).exists())
        # print(response_data)

        # sending request with invalid info
        invalid_transaction_info = {
            'name': 'test',
            'test': 'ting'
        }

        response = send_request(invalid_transaction_info, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)
        self.assertTrue(response_data.get('isError'))

    def testRead(self):
        ''' Testing transaction read '''

        url = '/transaction/read/'

        # sending request with valid transaction id
        valid_transaction_id = {
            'transactionId': 2
        }

        response = send_request(valid_transaction_id, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)

        # sending request with invalid transaction id
        invalid_transaction_id = {
            'transactionId': 1000
            # 'trasactionId': None
        }

        response = send_request(invalid_transaction_id, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)

    def testUpdate(self):
        ''' Testing transaction update '''
        url = '/transaction/update/'

        previous_transaction = models.Transaction.objects.get(pk=1)
        valid_transaction_info = {
            'transactionId': previous_transaction.id,
            'transactionInfo': {
                'product': 1,
                'stock': 1010,
                'note': 'updated transaction note'
            }
        }

        response = send_request(valid_transaction_info, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # check if updated product saved in database
        # print(response_data)

        invalid_transaction_info = {
            'transactionId': 100000,  # testing for id not in database
            # 'transactionId': None,
            'transactionInfo': {
                # 'product': 1,
                'stock': 20,
                'note': 'invalid note'
            }
        }

        response = send_request(invalid_transaction_info, url)
        response_data = loads(response.content).get('responseData')
        # print(response_data)
        self.assertTrue(response_data.get('isError'))

    def testDelete(self):
        ''' Testing transaction delete '''
        url = '/transaction/delete/'

        sending request with valid transaction id
        valid_transaction_id = {
            'transactionId': 2
        }

        response = send_request(valid_transaction_id, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)

        # sending request with invalid transaction id
        invalid_transaction_id = {
            'transactionId': 1002
        }

        response = send_request(invalid_transaction_id, url)
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # checking if response has errors
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

        transaction = models.Transaction.objects.get(pk=5)
        transaction_stock = transaction.stock
        product_id = transaction.product_id
        product = models.Product.objects.get(pk=product_id)
        product_stock = product.stock
        return_stock_data = {
            'transactionId': 5,
            'return_stocks': True
        }

        response = send_request(return_stock_data, url)
        self.assertEqual(response.status_code, 200)
        
        product_new_stock = models.Product.objects.get(pk=product_id).stock

        self.assertEqual(product_stock + transaction_stock, product_new_stock)





    def testLogicUpdate(self):
        ''' Testing transaction update logic '''
        url = '/transaction/update/'

        # testing updated logic when product is changed and return stocks is true
        transaction = models.Transaction.objects.get(pk=2)
        transaction_stock = transaction.stock
        changed_product = {
            'transactionId': 2,
            'transactionInfo': {
                'product': 2,
                'stock': 2000
            },
            'return_stocks': True
        }

        prev_prod_stock = models.Product.objects.get(
            pk=1).stock
        changed_prod_prev_stocks = models.Product.objects.get(pk=2).stock
        response = send_request(changed_product, url)
        self.assertEqual(response.status_code, 200)
        changed_prod_new_stocks = models.Product.objects.get(pk=2).stock
        prev_prod_new_stock = models.Product.objects.get(
            pk=1).stock

        # checks if stocks has returned to previous product
        self.assertEqual(prev_prod_stock - transaction_stock,
                         prev_prod_new_stock)

        # checks if new product stocks has changed
        self.assertEqual(changed_prod_new_stocks, changed_prod_prev_stocks +
                         changed_product.get('transactionInfo').get('stock'))

        response_data = loads(response.content).get('responseData')

        transaction = models.Transaction.objects.get(pk=3)
        prev_transaction_stock = transaction.stock
        prev_product = models.Product.objects.get(pk=transaction.product_id)
        prev_product_stock = prev_product.stock
        unchanged_product = {
            'transactionId': 3,
            'transactionInfo': {
                'product': 1,
                'stock': 3000
            }
        }

        response = send_request(unchanged_product, url)
        new_product_stock = models.Product.objects.get(pk=1).stock
        # checks if product stocks updated
        prev_product_stock_adjusted = prev_product_stock - prev_transaction_stock + unchanged_product.get('transactionInfo').get('stock')
        self.assertEqual(prev_product_stock_adjusted, new_product_stock)

        invalid_data = {
            'transactionId': 1,
            'transactionInfo': {
                'pr': None,
                'test': 'ok'
            }
        }

        response = send_request(invalid_data, url)
        response_data = loads(response.content).get('responseData')

        # print(response_data)
        self.assertTrue(response_data.get('isError'))

    def testLogicCreate(self):
        ''' Testing transaction create logic '''

        url = '/transaction/create/'
        product_stock = models.Product.objects.get(pk=2).stock
        
        valid_data = {
            'product': 2,
            'stock': 2000,
            'note': 'added 2000 stocks'
        }

        response = send_request(valid_data, url)
        new_product_stock = models.Product.objects.get(pk=2).stock
        self.assertEqual(product_stock + valid_data.get('stock'), new_product_stock)

    def testLogicDelete(self):
        ''' Testing transaction delete logic '''
        url = '/transaction/delete/'
        transaction = models.Transaction.objects.get(pk=2)
        transaction_stock = transaction.stock
        product_id = transaction.product_id
        product_stock = models.Product.objects.get(pk=product_id).stock
        
        valid_data = {
            'transactionId': 2,
            'return_stocks': True
        }

        response = send_request(valid_data, url)
        new_product_stock = models.Product.objects.get(pk=product_id).stock
        # check if product stock is returned 
        self.assertEqual(product_stock - transaction_stock, new_product_stock)
class QueryView(TestCase):
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

        # create 100 transaction
        for i in range(100):
            note = ''.join([random.choice(string.ascii_letters)
                            for i in range(10)])
            models.Transaction.objects.create(
                product_id=1, stock=random.randint(100, 1000), note=f'note {note}')

    def testProductQuery(self):
        ''' Testing product Query'''

        url = '/query/product/'
        # sending request with valid filters
        valid_filter = {
            'query': 'aa',
            'query_by': 'name',
            'query_limit': 100,
            'order_by': 'id',
            'order_type': 'ascn'
        }

        response = send_request(valid_filter, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)

        # sending request with invalid filters

        invalid_filter = {
            'query': 't',
            'query_by': 'test',
            'query_limit': 10,
            'order_by': 'test',
            'order_type': 'ascn',
        }

        response = send_request(invalid_filter, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))

        # print(response_data)

    def testSupplierQuery(self):
        ''' Testing supplier Query '''

        url = '/query/supplier/'
        valid_filter = {
            'query': '',
            'query_by': 'name',
            'query_limit': 2,
            'order_by': 'name',
            'order_type': 'desc'
        }

        response = send_request(valid_filter, url, 'GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        # print(response_data)

        invalid_filter = {
            'query': 't',
            'query_by': 'test',
            'order_type': 'ascn',
            'order_by': 'test'
        }

        response = send_request(invalid_filter, url, 'GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))
        # print(response_data)

    def testTransactionQuery(self):
        ''' Testing transaction Query'''
        url = '/query/transaction/'

        valid_filters = {
            'query': 'xb',
            # 'query_by_suffix': 'date',
            'query_by': 'note',
            # 'query_limit': 1,
            'order_type': 'desc',
            'order_by': 'created_on'
        }

        response = send_request(valid_filters, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')

        # print(response_data)

        invalid_filters = {
            'query_by': 'test',
            'order_type': 'desc',
            'order_by': 'tid',
        }

        response = send_request(invalid_filters, url, method='GET')
        self.assertEqual(response.status_code, 200)
        response_data = loads(response.content).get('responseData')
        self.assertTrue(response_data.get('isError'))

        # print(response_data)
