from django.contrib.auth.models import User, Group
from rest_framework import serializers

from eminisce.models.libraryuser import LibraryUser
from eminisce.models.book import Book
from eminisce.models.loans import Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class LibraryUserBioSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field="username",
    )

    class Meta:
        model = LibraryUser
        fields = ("user", "fingerprint", "face_front",)

class LibraryUserIDSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field="username",
    )

    class Meta:
        model = LibraryUser
        fields = ("user",)

class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("status",)

class CreateLoanSerializer(serializers.ModelSerializer):
    borrower = serializers.SlugRelatedField(
        queryset = LibraryUser.objects.all(),
        slug_field='user__username',
    )

    book = serializers.SlugRelatedField(
        queryset = Book.objects.all(),
        slug_field='barcode',
    )

    class Meta:
        model = Loan
        fields = ("borrower", "book", "start_date", "due_date")
