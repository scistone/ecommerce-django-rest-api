from rest_framework.generics import  ListAPIView,CreateAPIView,  RetrieveDestroyAPIView,RetrieveUpdateAPIView 
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser


from api.customer.serializers import CustomerSerializer
from users.models import User,Customer


        

class CustomerProfileView(ListAPIView):
    """
        Customer Profile
        
        PERM: IsAuthenticated
        AUTH: SessionAuth,TokenAuth 
        URL: api/customer/profile/
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.filter(user=request.user.id)
        if customer:
            return super().get(request, *args, **kwargs)            
        else:
            return Response({"Error":"You do not have a permission to make this request."},status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Customer.objects.filter(user=self.request.user.id)
        return queryset

class CustomerUpdateView(RetrieveUpdateAPIView):
    """
        Customer Update Profile
        
        PERM: IsAuthenticated
        AUTH: SessionAuth,TokenAuth 
        URL: api/profile/update
    """
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    serializer_class = CustomerSerializer
    # lookup_field = "user_id"

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.filter(user=request.user.id)
        if customer :
            return super().get(request, *args, **kwargs)            
        else:
            return Response({"Error":"You do not have a permission to make this request."},status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(user_id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj 
    

    def put(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=self.request.user.id)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Error"} ,status=status.HTTP_400_BAD_REQUEST)
