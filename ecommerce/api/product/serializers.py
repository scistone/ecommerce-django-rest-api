from rest_framework import serializers
from product.models import Product



class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'barcode',
            'categories',
            'image',
            'color',
            'size',
            'model_code',
            'description',
            'slug',
            'meta_description',
            'date_created',
            'price',
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'barcode',
            'categories',
            'color',
            'size',
            'model_code',
            'description',
            'slug',
            'meta_description',
            'date_created',
            'price',
            'get_image',
            'get_thumbnail'
        ]