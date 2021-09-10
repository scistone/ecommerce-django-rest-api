from django.urls import path,include


from .views import (
        CreateCollectionAPIView,
        CollectionUpdateAPIView,
        CollectionDeleteAPIView,

        CreateProductAPIView,
        ProductUpdateAPIView,

        CreateMenuAPIView,
        CreateMenuElementAPIView,

        BlogPostCreateAPIView,
        BlogPostUpdatePIView
)

urlpatterns = [
    path('menu/add/',CreateMenuAPIView.as_view(),  name='create_collection'),
    path('menu/element/add/',CreateMenuElementAPIView.as_view(),  name='create_collection'),

    path('collection/add/',CreateCollectionAPIView.as_view(),  name='create_collection'),
    path('collection/update/<slug>/',CollectionUpdateAPIView.as_view(),  name='update_collection'),
    path('collection/delete/<slug>/',CollectionDeleteAPIView.as_view(),  name='delete_collection'),
    
    path('product/add/',CreateProductAPIView.as_view(),  name='create_product'),
    path('product/update/<slug>',ProductUpdateAPIView.as_view(),  name='update_product'),

    path('blog-post/add/',BlogPostCreateAPIView.as_view(),  name='create_blog_post'),
    path('blog-post/update/<slug>',BlogPostUpdatePIView.as_view(),  name='update_blog_post'),
]