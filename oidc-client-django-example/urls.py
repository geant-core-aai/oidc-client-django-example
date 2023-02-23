from django.urls import path
from oidc_client import views

urlpatterns = [
    path('', views.welcome),
    path('redirect', views.home)
]
