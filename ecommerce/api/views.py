#RestFramework
from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
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
from core.models import Menu
from .serializers import (
        CollectionSerializer,
        CreateProductSerializer,
        ProductSerializer,
        MenuSerializer
)



class ListProductAPIView(ListAPIView):
    """

    Method: GET
    URL: /api/products/

    """
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id','title','description','slug','model_code','collections']
    ordering_fields = ['id']

class ProductDetailAPIView(APIView):
    """

    Method: GET
    URL: product/<model_code>/<product_slug>/

    """
    permission_classes = [AllowAny]
    def get(self, request, model_code, product_slug, format=None):
        product = Product.objects.filter(model_code=model_code)
        product = get_object_or_404(product,slug=product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CollectionListAPIView(ListAPIView):
    """

    Method: GET
    URL: /api/collections/

    """
    queryset = Collection.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    serializer_class = CollectionSerializer

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id','name','description','slug']
    ordering_fields = ['id']

class MenuListView(ListAPIView):
    serializer_class        = MenuSerializer
    permission_classes      = [AllowAny]
    queryset                = Menu.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["menu_type"]
