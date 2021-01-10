from django.db import models
from store.models import Product
from accounts.models import Customer
# Create your models here.


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=False, default=0)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
