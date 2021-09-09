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
from api.serializers import CollectionSerializer,CreateProductSerializer


class CreateCollectionAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/collection/add/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer


class CollectionUpdateAPIView(RetrieveUpdateAPIView):
    """

    Method: GET,PUT
    URL: /api/collection/update/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'


class CollectionDeleteAPIView(RetrieveDestroyAPIView):
    """

    Method: DELETE
    URL: /api/collection/delete/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'

class CreateProductAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/collection/add/

    """
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateProductSerializer

###########################
class ProductUpdateAPIView(RetrieveUpdateAPIView):
    """

    Method: GET,PUT
    URL: /api/product/update/<slug>/

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
    queryset = Menu.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateMenuSerializer

class CreateMenuElementAPIView(CreateAPIView):
    queryset = MenuElement.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateMenuElementSerializer