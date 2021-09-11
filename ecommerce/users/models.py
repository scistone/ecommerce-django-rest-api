from django.db import models

import jwt

from datetime import datetime, timedelta
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    username    = None

    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email   

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.email


    def get_full_name(self):
        return (self.first_name + self.last_name)

    def get_short_name(self):
        return self.first_name


class CustomerAddress(models.Model):
    ADDRESS_TYPES = [
        ('B','Billing Address'),
        ('S','Shipping Address'),
    ]
    customer                = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,editable=False)
    first_name              = models.CharField(max_length=100)
    last_name               = models.CharField(max_length=100)
    phone                   = models.CharField(verbose_name="phone",max_length=10)
    address                 = models.TextField(max_length=100)
    zip_code                = models.CharField(max_length=7,null=True,blank=True)
    city                    = models.CharField(max_length=100)
    district                = models.CharField(max_length=100)
    country                 = models.CharField(max_length=100)
    last_used               = models.DateTimeField(verbose_name='last action', auto_now=True)
    address_type            = models.CharField(choices=ADDRESS_TYPES,max_length=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.adresss} {self.city}/{self.district} {self.zip_code}"

