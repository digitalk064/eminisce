from django.contrib.auth.models import User, Group
from rest_framework import serializers

from eminisce.models.book import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
