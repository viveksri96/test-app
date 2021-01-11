from django.db import models
from store.models import Product
from accounts.models import Customer

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
