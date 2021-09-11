from django.urls import path,include

urlpatterns = [
    path('address/create/', CreateCustomerAddressAPIView.as_view(), name="create_customer_address"),
]