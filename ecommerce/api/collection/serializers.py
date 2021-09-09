from rest_framework import serializers

from product.models import Collection
from api.product.serializers import ProductSerializer

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        ordering = ['-id']
        fields = [
            'id',
            'name',
            'image',
            'slug',
            'description',
            'meta_description',
        ]
        extra_kwargs = {'id': {'read_only':True},}
