#RestFramework
from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser

from rest_framework.authentication import SessionAuthentication

#Django Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


#Knox Authentication Class
from knox.auth import TokenAuthentication

#Serializers & Models
from product.models import Collection
from .serializers import CollectionSerializer


class CreateCollectionAPIView(CreateAPIView):
    """

    Method: POST
    URL: /api/collection/add/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = CollectionSerializer


class CollectionListAPIView(ListAPIView):
    """

    Method: GET
    URL: /api/collection/list/

    """
    queryset = Collection.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    serializer_class = CollectionSerializer

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id','name','description','slug']
    ordering_fields = ['id']

class CollectionUpdateAPIView(RetrieveUpdateAPIView):
    """

    Method: GET,PUT
    URL: /api/collection/update/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'


class CollectionDeleteAPIView(RetrieveDestroyAPIView):
    """

    Method: DELETE
    URL: /api/collection/delete/<slug>/

    """
    queryset = Collection.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = CollectionSerializer
    lookup_field = 'slug'
