from django.urls import path,include


from .views import CollectionListAPIView,ListProductAPIView,ProductDetailAPIView


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('sellercentral/', include('api.sellercentral.urls')),
    


    path('collections/' ,  CollectionListAPIView.as_view(),  name='categories'),
    path('products/' ,  ListProductAPIView.as_view(),  name='products'),
    path('products/detail/<model_code>/<product_slug>', ProductDetailAPIView.as_view(), name='product-detail'),
]
