from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, mixins
from .serializers import BookSerializer

from eminisce.models.book import Book

#Only allow getting book info, not updating them
class BookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'barcode'
