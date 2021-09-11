from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView,GenericAPIView,UpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from knox.models import AuthToken

from users.models import User
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer,ChangePasswordSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
#Register
from knox.auth import TokenAuthentication

from django.contrib.auth import login

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        instance, token = AuthToken.objects.create(user)
        login(request, user)
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
        login(request, user)
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

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from api.utils import Util


class RequestPasswordResetEmailView(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def create_link(self,user):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        #current_site = FRONTEND URL
        
        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        absurl = 'http://' + current_site + relativeLink

        return absurl
    
    def create_emaildata(self,absurl):
        email_body = 'Hello, \n Use link below to reset your password  \n'+absurl
            
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset your passsword'
        }
        return data

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            link = self.create_link(user=user)
            data = self.create_emaildata(absurl=link)
            
            Util.send_email(data)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'E-mail does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            
            success = {
                'success' : True,
                'message' : 'Credentials Valid',
                'uidb64'  : uidb64,
                'token'   : token 
            }
            return Response(success, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)