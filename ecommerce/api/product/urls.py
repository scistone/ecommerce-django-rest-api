from django.urls import path,include


from .views import CreateProductAPIView,ListProductAPIView

urlpatterns = [
    path('list/' ,  ListProductAPIView.as_view(),  name='products'),
    path('add/',CreateProductAPIView.as_view(),  name='create_product'),
]