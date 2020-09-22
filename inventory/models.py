from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    barcode = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()
    note = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.product.stock = self.product.stock + self.stock
        super(Transaction, self).save(self, *args, **kwargs)



