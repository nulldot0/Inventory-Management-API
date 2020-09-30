from django.db import models
from django.core.exceptions import FieldError, ValidationError


class QuerySet(models.QuerySet):
    def search(self, **kwargs):
        ''' This function is responsible for searching '''
        q = self  # the query objects
        errors = []  # error collection
        if kwargs.get('query_by'):
            try:
                query = kwargs.get('query')
                query_by = {
                    f'{kwargs.get("query_by")}__icontains': query
                }

                q = q.filter(**query_by)
            except FieldError as e:
                errors.append(e.args[0])

        if kwargs.get('order_type') == 'desc':
            # order product ascending or descending with it's order_by value
            # (e.g. order_by = "stock", order_by="name", order_by="stock")
            # order_type has two choices only desc or ascn

            if kwargs.get('order_by'):
                order_by = f'-{kwargs["order_by"]}'
                # error checking if field name exists in the model
                try:
                    q = q.order_by(order_by)
                except FieldError as e:
                    errors.append(e.args[0])

        elif kwargs.get('order_type') == 'ascn':
            if kwargs.get('order_by'):
                order_by = f'{kwargs["order_by"]}'
                # error checking if field name exists in the model
                try:
                    q = q.order_by(
                        kwargs['order_by'])
                except FieldError as e:
                    errors.append(e.args[0])

        if kwargs.get('query_limit'):
            # limit query with query_limit value
            q = q[0:kwargs['query_limit']]

        if errors:
            # return this if there are errors
            return {
                'isError': True,
                'errorInfo': errors
            }
        else:
            return q


class TransactionQuerySet(models.QuerySet):
    def search(self, **kwargs):
        q = self
        errors = []
        query = kwargs.get('query')

        if kwargs.get('query_by') == 'created_on':
            suffix = kwargs.get('query_by_suffix')
            try:
                if suffix == 'range':
                    # if suffix is ranges then split and strip query
                    query = [i.strip() for i in query.split(',')]

                try:
                    query_by = {
                        f'{kwargs.get("query_by")}__{suffix}': query
                    }
                    q = q.filter(**query_by)
                except ValidationError as e:
                    errorInfo = str(e.args[0] % e.args[-1])
                    errors.append(errorInfo)

            except FieldError as e:
                errors.append(e.args[0])

        if kwargs.get('query_by') != 'created_on':
            try:
                query_by = {
                    f'{kwargs.get("query_by")}__icontains': query
                }

                q = q.filter(**query_by)
            except FieldError as e:
                errors.append(e.args[0])

        if kwargs.get('order_type') == 'desc':
            if kwargs.get('order_by'):
                order_by = f'-{kwargs["order_by"]}'
                # try to order queries from given "order_by" value
                try:
                    q = q.order_by(order_by)
                except FieldError as e:
                    errors.append(e.args[0])

        elif kwargs.get('order_type') == 'ascn':
            if kwargs.get('order_by'):
                order_by = kwargs["order_by"]
                # try to order queries from given "order_by" value
                try:
                    q = q.order_by(order_by)
                except FieldError as e:
                    errors.append(e.args[0])

        if kwargs.get('query_limit'):
            query_limit = kwargs.get('query_limit')
            q = q[0:query_limit]

        if errors:
            return {
                'isError': True,
                'errorInfo': errors
            }

        else:
            return q


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=100)

    objects = QuerySet.as_manager()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    barcode = models.CharField(max_length=100, blank=True, unique=True)
    stock = models.IntegerField(default=0)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True)

    objects = QuerySet.as_manager()


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()
    note = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now=True)

    objects = TransactionQuerySet.as_manager()
