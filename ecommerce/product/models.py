from io import BytesIO
from PIL import Image
from django.core.files import File

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


class Product(models.Model):
    categories      = models.ManyToManyField(Collection,blank=True)
    barcode         = models.CharField(max_length=20)
    title           = models.CharField(max_length=144)
    thumbnail       = models.ImageField(upload_to='uploads/',blank=True,null=True)
    image           = models.ImageField(upload_to='uploads/',blank=True,null=True)
    color           = models.CharField(max_length=20,blank=True,null=True)
    size            = models.CharField(max_length=20,blank=True,null=True)
    model_code      = models.CharField(max_length=20)
    description     = models.TextField(blank=True,null=True)
    slug            = models.SlugField(unique=True,max_length=150,editable=False)
    meta_description= models.CharField(max_length=144,editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    price           = models.DecimalField(max_digits=6,decimal_places=2)

    def get_slug(self):
        slug   = slugify(self.title.replace("ı","i"))
        unique = slug
        number = 1
        while Product.objects.filter(slug=unique).exists():
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

        return super(Product,self).save(*args,**kwargs)
        
    def get_absolute_url(self):
        return f'product/detail/{self.model_code}/{self.slug}'

    def __str__(self):
        return self.title
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
                

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail