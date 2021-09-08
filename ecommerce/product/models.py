from io import BytesIO

from PIL import Image

from django.db import models
from django.utils.text import slugify


# Create your models here.


class Collection(models.Model):
    name                = models.CharField(max_length=100)
    image               = models.ImageField(upload_to="uploads/",blank=True,null=True)
    slug                = models.SlugField(unique=True,max_length=150,editable=False)
    description         = models.TextField(null=True,blank=True)
    meta_description    = models.CharField(max_length=144,editable=False)
    date_created        = models.DateTimeField(auto_now_add=True,editable=False)

    def get_slug(self):
        slug   = slugify(self.name.replace("ı","i"))
        unique = slug
        number = 1
        while Collection.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique
    
    def save(self,*args,**kwargs):
        if len(self.description) > 144:
            self.meta_description = self.description[:144]
        else :
            self.meta_description = self.description

        if self.slug == "":
            self.slug = self.get_slug()
            
        return super(Collection,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag         = models.CharField(unique=True,primary_key=True,max_length=100)
    def __str__(self):
        return f"{self.tag}"

class Media(models.Model):
    MEDIA_TYPES = [
        ('I','Image'),
        ('V','Video')
    ]
    slug            = models.CharField(max_length=150)
    media_type      = models.CharField(choices=MEDIA_TYPES,max_length=1)
    image           = models.FileField(upload_to="uploads/",blank=True,null=True)

class Brand(models.Model):
    title       = models.CharField(max_length=144,unique=True)
    logo        = models.URLField(null=True,blank=True) #default store logo
    is_active   = models.BooleanField(default=False,editable=False)

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    categories      = models.ForeignKey(Collection,on_delete=models.SET_NULL,related_name='products',null=True)
    barcode         = models.CharField(max_length=20)
    title           = models.CharField(max_length=144)
    brand           = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    thumbnail       = models.URLField()
    color           = models.CharField(max_length=20,blank=True,null=True)
    size            = models.CharField(max_length=20,blank=True,null=True)
    model_code      = models.CharField(max_length=20)
    description     = models.TextField(blank=True,null=True)
    slug            = models.SlugField(unique=True,max_length=150,editable=False)
    meta_description= models.CharField(max_length=144,editable=False)
    tags            = models.ManyToManyField(Tag,blank=True)
    medias          = models.ManyToManyField(Media,blank=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    price           = models.DecimalField(max_digits=6,decimal_places=2)

    def get_slug(self):
        slug   = slugify(self.title.replace("ı","i"))
        unique = slug
        number = 1
        while Item.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique

    def save(self,*args,**kwargs):
        if len(self.description) > 144:
            self.meta_description = self.description[:144]
        else :
            self.meta_description = self.description

        if self.slug == "":
            self.slug = self.get_slug()

        return super(Item,self).save(*args,**kwargs)
        
    def get_absolute_url(self):
        return f'/{self.slug}/'

    def __str__(self):
        return self.title

