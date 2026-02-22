from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)
    image = models.CharField()

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    is_active = models.BooleanField()
    slug = models.SlugField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


