from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomerAddressSerializer
from users.models import CustomerAddress

class CreateCustomerAddressAPIView(CreateAPIView):
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]
    