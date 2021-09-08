from django.urls import path,include


from .views import CreateCollectionAPIView,CollectionListAPIView,CollectionUpdateAPIView,CollectionDeleteAPIView

urlpatterns = [
    path('list/' ,  CollectionListAPIView.as_view(),  name='categories'),
    path('add/',CreateCollectionAPIView.as_view(),  name='create_collection'),
    path('update/<slug>/',CollectionUpdateAPIView.as_view(),  name='update_collection'),
    path('delete/<slug>/',CollectionDeleteAPIView.as_view(),  name='delete_collection'),
]