from django.db import models

# Create your models here.
from product.models import Product
from users.models import User

class Order(models.Model):
    ORDER_STATUS = [
        ('P','Paid'),
        ('W','Waiting for payment'),
        ('E','Error')
    ]
    user        = models.ForeignKey(User,related_name='orders',on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    email       = models.CharField(max_length=100)
    address     = models.CharField(max_length=100)
    city        = models.CharField(max_length=100)
    country     = models.CharField(max_length=100)
    zip_code    = models.CharField(max_length=100)
    phone       = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    iyzico_token= models.CharField(max_length=200)
    order_status=models.CharField(max_length=1,choices=ORDER_STATUS,default="W")

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='product',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        return super(OrderItem,self).save(*args,**kwargs)

    def __str__(self):
        return self.id
