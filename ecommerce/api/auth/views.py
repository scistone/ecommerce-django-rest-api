from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView,GenericAPIView,UpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from knox.models import AuthToken

from users.models import User
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer,ChangePasswordSerializer
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
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def get_object(self):
        return self.request.user

class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=User):
        return self.request.user


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def get_object(self, queryset=User):
        return self.request.user
