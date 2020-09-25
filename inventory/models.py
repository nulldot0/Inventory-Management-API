from django.db import models
from django.db.models.functions import Coalesce


class ProductQuerySet(models.QuerySet):

    def search(self, **kwargs):
        ''' This function is responsible for searching product '''
        product_searched = self # the Product objects
        if kwargs.get('query', ''):
            query = kwargs['query'] # the query to search
            if kwargs.get('query_by') == 'description':
                product_searched = product_searched.filter(
                    description__icontains=query)
            elif kwargs.get('query_by') == 'stock':
                # filter products with query in barcode
                try:
                    query = int(query)
                except:
                    query = -1

                product_searched = product_searched.filter(stock=query)
            elif kwargs.get('query_by') == 'barcode':
                # filter products with query in barcode
                product_searched = product_searched.filter(
                    barcode__icontains=query)
            else:
                # filter products with query in name
                product_searched = product_searched.filter(
                    name__icontains=kwargs['query'])

        if kwargs.get('order_type'):
            # order product ascending or descending with it's order_by value
            # (e.g. order_by = "stock", order_by="name", order_by="stock") 
            # order_type has two choices only desc or ascn

            if kwargs.get('order_type') == 'desc':
                order_by = f'-{kwargs["order_by"]}'
                product_searched = product_searched.order_by(order_by)
            else:
                order_by = f'{kwargs["order_by"]}'
                product_searched = product_searched.order_by(
                    kwargs['order_by'])

        if kwargs.get('query_limit'):
            # limit query with query_limit value
            product_searched = product_searched[0:kwargs['query_limit']]

        return product_searched


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    barcode = models.CharField(max_length=100, blank=True, unique=True)
    stock = models.IntegerField(default=0)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True)

    objects = ProductQuerySet.as_manager()


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()
    note = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.product.stock = self.product.stock + self.stock
        super(Transaction, self).save(self, *args, **kwargs)
