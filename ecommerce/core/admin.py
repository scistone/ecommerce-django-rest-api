from django.contrib import admin

# Register your models here.
from .models import Menu,MenuElement


admin.site.register(Menu)
admin.site.register(MenuElement)