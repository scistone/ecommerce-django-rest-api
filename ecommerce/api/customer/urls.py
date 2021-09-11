from django.urls import path,include


from .views import (
    CustomerUpdateView
)

urlpatterns = [
    path('profile/', CustomerUpdateView.as_view(), name="profile"),
]
