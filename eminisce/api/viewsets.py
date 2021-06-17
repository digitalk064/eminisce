from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, mixins
from .serializers import BookSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from eminisce.models.book import Book

#Only allow getting book info, not updating them
class BookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer
    lookup_field = 'barcode'
