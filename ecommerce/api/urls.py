from django.urls import path,include


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('collection/', include('api.collection.urls'))
]
