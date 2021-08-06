#Rest
from django.urls import include, path
from rest_framework import routers
from . import viewsets
from .views import loans

router = routers.DefaultRouter()

router.register(r'books', viewsets.BookViewSet)
router.register(r'libraryusersbio', viewsets.LibraryUserBioViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('loans/new_loan', loans.new_loan),
    path('loans/update_loan/<int:pk>', loans.update_loan),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]