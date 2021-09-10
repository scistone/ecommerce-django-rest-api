from django.urls import path,include


from .views import (
        CollectionListAPIView,
        ListProductAPIView,
        ProductDetailAPIView,
        MenuListView,
        BlogPostListAPIView,
        BlogPostDetailAPIView
)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('sellercentral/', include('api.sellercentral.urls')),
    
    

    path('menu/', MenuListView.as_view(), name='menu'),
    path('collections/',  CollectionListAPIView.as_view(),  name='categories'),
    path('products/',  ListProductAPIView.as_view(),  name='products'),
    path('product/<model_code>/<product_slug>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('blog-posts/',  BlogPostListAPIView.as_view(),  name='blog_posts'),
    path('blog-post/<slug>/',  BlogPostDetailAPIView.as_view(),  name='blog_post_detail'),
]
