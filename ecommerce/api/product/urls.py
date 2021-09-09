from django.urls import path,include


from .views import CreateProductAPIView,ListProductAPIView,ProductDetailAPIView

urlpatterns = [
    path('list/' ,  ListProductAPIView.as_view(),  name='products'),
    path('add/',CreateProductAPIView.as_view(),  name='create_product'),
    path('detail/<model_code>/<product_slug>', ProductDetailAPIView.as_view(), name='product-detail'),
]