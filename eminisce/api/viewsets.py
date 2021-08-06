from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, mixins
from .serializers import BookSerializer, LibraryUserBioSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser

#Only allow getting book info, not updating them
class BookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer
    lookup_field = 'barcode'

class LibraryUserBioViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = LibraryUser.objects.all().order_by("user").exclude(fingerprint__isnull=True).exclude(fingerprint__exact=b'').exclude(face_front__isnull=True).exclude(face_front__exact=b'')
    serializer_class = LibraryUserBioSerializer
    lookup_field = 'user'

