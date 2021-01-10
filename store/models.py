from django.db import models
from accounts.models import User
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100, null=False)
    address = models.TextField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)


class Product(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=False, default='')
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to="uploads/")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
