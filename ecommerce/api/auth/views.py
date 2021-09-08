from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import RetrieveAPIView,GenericAPIView

from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from knox.models import AuthToken

from users.models import User
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
#Register
from knox.auth import TokenAuthentication

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        instance, token = AuthToken.objects.create(user)
        
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : token
        })
    
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email', None)

        user = User.objects.get(email=email)

        instance, token = AuthToken.objects.create(user)
        
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : token
        })

class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        print(self.request)
        return self.request.user
