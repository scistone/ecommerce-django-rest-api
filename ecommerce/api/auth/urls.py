from django.urls import path,include


from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import (
    RegisterAPIView,
    LoginAPIView,
    UserAPIView,
    ChangePasswordView,
    UserUpdateAPIView,
    RequestPasswordResetEmailView,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView
)

from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="create_user"),
    path('login/', LoginAPIView.as_view(), name="login_view"),
    path('logout/', knox_views.LogoutView.as_view(), name="knox_logout"),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name="login_view"),
    path('user/', UserAPIView.as_view(), name="user"),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('user/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('request-reset-email/', RequestPasswordResetEmailView.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]
