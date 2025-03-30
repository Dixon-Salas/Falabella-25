from django.db import models
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value < 0:
        raise ValidationError(f'{value} El precio debe ser un numero positivo.')


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images', null=True, blank=True)
    specifications = models.JSONField(default=dict)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    sold_quantity = models.PositiveIntegerField(default=0)
    shipping_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name