from rest_framework import serializers

#Collection Serializer
from product.models import Collection
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        ordering = ['-id']
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'meta_description',
        ]
        extra_kwargs = {'id': {'read_only':True},}


#Product Serializers
from product.models import Product
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'barcode',
            'collections',
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
    collections = CollectionSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'barcode',
            'collections',
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