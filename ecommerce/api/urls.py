from django.urls import path,include


from .views import (
        CollectionListAPIView,
        ListProductAPIView,
        ProductDetailAPIView,
        MenuListView,
)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('sellercentral/', include('api.sellercentral.urls')),
    
    

    path('menu/', MenuListView.as_view(), name='menu'),
    path('collections/',  CollectionListAPIView.as_view(),  name='categories'),
    path('products/',  ListProductAPIView.as_view(),  name='products'),
    path('product/<model_code>/<product_slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
