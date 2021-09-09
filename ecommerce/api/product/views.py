#RestFramework
from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
#Django Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


#Knox Authentication Class
from knox.auth import TokenAuthentication

from product.models import Product
from.serializers import CreateProductSerializer,ProductSerializer

class CreateProductAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/collection/add/

    """
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CreateProductSerializer


class ListProductAPIView(ListAPIView):
    """

    Method: GET
    URL: /api/product/all/

    """
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id','title','description','slug','model_code','categories']
    ordering_fields = ['id']

class ProductDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, model_code, product_slug, format=None):
        product = Product.objects.filter(model_code=model_code)
        product = get_object_or_404(product,slug=product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)