from email.mime import base
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('items', views.OrderViewSet, basename='order')


app_name = 'order'
urlpatterns = [
    path('', include(router.urls))
]