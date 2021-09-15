from django.urls import path

from .views import CreateOrderView,PaymentCallbackAPIView,CheckPaymentAPIView

urlpatterns = [
    path('checkout/',CreateOrderView.as_view()),
    path('payment-callback/',PaymentCallbackAPIView.as_view()),
    path('check-order-payment/<token>', CheckPaymentAPIView.as_view(), name='check-order-payment'),
]

