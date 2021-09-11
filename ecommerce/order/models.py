from django.db import models

# Create your models here.

from users.models import Customer
from product.models import Product

class CartItem(models.Model):
    STATUS_MEANS = [
        ('0','Shopping'),
        ('1','Waiting for payment'),
        ('2','Sold'),
        ('3','Deleted'),
    ]
    customer        = models.ForeignKey(Customer,on_delete=models.CASCADE,editable=False,null=True)
    product         = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity        = models.IntegerField(default=1)
    is_reserved     = models.BooleanField(default=0)
    price           = models.FloatField(default=0,blank=True)#,editable=False
    status          = models.CharField(max_length=1,choices=STATUS_MEANS,default="0",editable=False)
    time_added      = models.DateTimeField(verbose_name='date added',auto_now_add=True)
    
    def stock_control(self):
        remaining = self.product.stock - self.quantity
        if remaining < 0 :
            return False
        return True

    def delete(self,*args,**kwargs):
        self.status = 3
        return self.save(*args,**kwargs)

    def __str__(self):
        return f"{self.id} {self.customer} {self.get_status_display()}"

class Order(models.Model):
    STATUS_MEANS = [
        ('0','Waiting for Payment'),
        ('1','Paid'),
        ('2','Not Paid')
    ]
    order_no            = models.IntegerField(unique=True,editable=False)
    customer            = models.ForeignKey(Customer,on_delete=models.CASCADE)
    cart_items          = models.ManyToManyField(CartItem)
    status              = models.CharField(max_length=1,choices=STATUS_MEANS,default="0")
    
    #address
    shippingAddress_first_name = models.CharField(max_length=100)
    shippingAddress_last_name  = models.CharField(max_length=100)
    shippingAddress_phone      = models.CharField(max_length=10)
    shippingAddress_address    = models.TextField()
    shippingAddress_zip        = models.CharField(max_length=100)
    shippingAddress_city       = models.CharField(max_length=100)
    shippingAddress_country    = models.CharField(max_length=100)


    billingAddress_first_name  = models.CharField(max_length=100)
    billingAddress_last_name   = models.CharField(max_length=100)
    billingAddress_phone       = models.CharField(max_length=10)
    billingAddress_address     = models.TextField()
    billingAddress_zip         = models.CharField(max_length=100)
    billingAddress_city        = models.CharField(max_length=100)
    billingAddress_country     = models.CharField(max_length=100)

    coupon              = models.CharField(max_length=155,blank=True,null=True)
    created             = models.DateTimeField(verbose_name='date created',auto_now_add=True)
    modified            = models.DateTimeField(verbose_name='date modified',auto_now=True)
    total_amount        = models.FloatField(editable=False,default=0.0)
    amount              = models.FloatField(editable=False,default=0.0)
    paid_amount         = models.FloatField(editable=False,default=0)
    returned_amount     = models.FloatField(editable=False,default=0.0)

    def cart_items_is_valid(self):
        for cart_item in self.cart_items.all():
            if cart_item.customer != self.customer:
                raise ValidationError("Cart item not valid")
    
    def generate_order_no(self):
        number = 1000
        while Order.objects.filter(order_no=number).exists():
            number += 1
        return number
    
    def save(self,*args,**kwargs):
        if self.order_no is None:
            self.order_no = self.generate_order_no()
            
        return super(Order,self).save(*args,**kwargs)

    
    def __str__(self):
        return f"Order No: {self.order_no} -  {self.customer} Total: {self.amount} Returned Amount: {self.returned_amount}"
