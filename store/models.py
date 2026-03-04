from django.db import models

from api import settings



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
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    slug = models.SlugField(max_length=50,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cart','product')


ORDER_STATUS = [
    ("pending","Pending"),
    ("paid","Paid"),
    ("cancelled","Cancelled")
]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(choices=ORDER_STATUS,default="pending",max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def calc_total(self):
        return sum(item.quantity * item.price_at_purchase for item in self.items.all())
        

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10,decimal_places=2)

    