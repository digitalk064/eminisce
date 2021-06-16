#Rest
from django.urls import include, path
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()

router.register(r'books', viewsets.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]