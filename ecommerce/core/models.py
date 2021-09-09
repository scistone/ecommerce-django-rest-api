from django.db import models

# Create your models here.
from product.models import Collection

class Menu(models.Model):
    MENU_TYPES = [
        ('main','Main Menu'),
        ('left','Hamburger Menu'),
    ]
    title       = models.CharField(max_length=144)
    category    = models.ForeignKey(Collection,on_delete=models.CASCADE,blank=True,null=True)
    menu_type   = models.CharField(max_length=4,choices=MENU_TYPES)
    priority    = models.IntegerField()
    
    def __str__(self):
        return self.title

class MenuElement(models.Model):
    title       = models.CharField(max_length=144)
    category    = models.ForeignKey(Collection,on_delete=models.CASCADE,blank=True,null=True)
    priority    = models.IntegerField()
    parent      = models.ForeignKey(Menu,on_delete=models.CASCADE)
    def __str__(self):
        return self.title