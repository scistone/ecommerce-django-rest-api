#RestFramework
from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

#Django Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


#Knox Authentication Class
from knox.auth import TokenAuthentication

#Serializers & Models
from product.models import Collection,Product
from api.serializers import CollectionSerializer,CreateProductSerializer,BlogPostSerializer


class CreateCollectionAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/sellercentral/collection/add/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer


class CollectionUpdateAPIView(RetrieveUpdateAPIView):
    """

    Method: GET,PUT
    URL: /api/sellercentral/collection/update/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'


class CollectionDeleteAPIView(RetrieveDestroyAPIView):
    """

    Method: DELETE
    URL: /api/sellercentral/collection/delete/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'

###########################
class CreateProductAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/sellercentral/collection/add/

    """
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateProductSerializer


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    """

    Method: GET,PUT
    URL: /api/sellercentral/product/update/<slug>/

    """
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateProductSerializer
    lookup_field = 'slug'

################################
from core.models import Menu,MenuElement
from .serializers import CreateMenuElementSerializer,CreateMenuSerializer

class CreateMenuAPIView(CreateAPIView):
    """
    
    Method: POST
    URL : api/sellercentral/menu/add/

    """


    queryset = Menu.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateMenuSerializer

class CreateMenuElementAPIView(CreateAPIView):
    """
    
    Method: POST
    URL : api/sellercentral/menu/element/add/

    """
    queryset = MenuElement.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateMenuElementSerializer


from core.models import BlogPost

class BlogPostCreateAPIView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
        return serializer

class BlogPostUpdatePIView(RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"
    
    def perform_update(self,serializer):
        serializer.save(modified_by=self.request.user)
        return serializer