from django.db import models

# Create your models here.
from product.models import Collection
from users.models import User

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

from django.utils.text import slugify

class BlogPost(models.Model):
    title       = models.CharField(max_length=144)
    content     = models.TextField()
    author      = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    created_at  = models.DateTimeField(editable=False,auto_now_add=True)
    modified_at = models.DateTimeField(editable=False,auto_now=True)
    slug        = models.SlugField(unique=True,max_length=150,editable=False)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="updated_by",null=True)

    def get_slug(self):
        slug   = slugify(self.title.replace("ı","i"))
        unique = slug
        number = 1
        while BlogPost.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique

    def save(self,*args,**kwargs):
        if self.slug == "":
            self.slug = self.get_slug()

        return super(BlogPost,self).save(*args,**kwargs)