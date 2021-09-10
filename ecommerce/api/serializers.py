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

#Menu Serializer
from core.models import Menu,MenuElement
class MenuElementSerializer(serializers.ModelSerializer):
    category        = serializers.SerializerMethodField()
    category_id     = serializers.SerializerMethodField()
    class Meta:
        model = MenuElement
        ordering = ['-priority']
        fields = [
            "title",
            "category_id",
            "category",
            "priority",
        ]
    
    def get_category(self,obj):
        return obj.category.slug
    def get_category_id(self,obj):
        return obj.category.id

class MenuSerializer(serializers.ModelSerializer):
    childs  = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        ordering = ['-priority']
        fields = [
            "title",
            "category_id",
            "category",
            "priority",
            "menu_type",
            "childs"
        ]
    def get_category(self,obj):
        return obj.category.slug
    def get_category_id(self,obj):
        return obj.category.id
    
    def get_childs(self,obj):
        queryset            = MenuElement.objects.filter(parent=obj.id)
        menuElementSerializer  = MenuElementSerializer(queryset,many=True).data
        return menuElementSerializer

from users.models import User

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ["get_full_name"]

from core.models import BlogPost
class BlogPostSerializer(serializers.ModelSerializer):
    author = UserEmailSerializer(read_only=True)
    modified_by = UserEmailSerializer(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'content',
            'author',
            'created_at',
            'modified_at',
            'slug',
            'modified_by'
        ]