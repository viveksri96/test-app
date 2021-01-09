from django.db import models
from accounts.models import User
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    mrp = models.DecimalField(max_digit=10, decimal_places=2, null=False, blank=False)
    sale_price = models.DecimalField(max_digit=10, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to="uploads/")

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
class ProductCategoryMap(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)