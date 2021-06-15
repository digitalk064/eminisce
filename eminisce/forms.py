from django.forms import ModelForm
from django.forms import inlineformset_factory

from .models.book import Book, Author, BookBarcode
from .models.libraryuser import LibraryUser

from django import forms

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

#AuthorFormSet = inlineformset_factory(Author, Book, form=AuthorForm, can_delete=False)

class LibraryUserForm(ModelForm):

    idnum = forms.CharField(label="Identification Number", help_text="Can be Student ID or Employee ID, used for logging in.")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LibraryUser
        fields = ['idnum', 'password', 'fullname', 'user_type']
        exclude = ['status', 'user']

class LibraryUserEditForm(ModelForm):

    idnum = forms.CharField(label="Identification Number", help_text="Can be Student ID or Employee ID, used for logging in.")
    fingerprint_upload = forms.FileField(widget=forms.FileInput(attrs={'accept': '.bmp, .jpg'}), 
    required=False, help_text="Upload fingerprint file generated from the fingerprint reader.")

    class Meta:
        model = LibraryUser
        fields = ['idnum', 'fullname', 'user_type', 'status', 'fingerprint_upload']
        exclude = ['user']