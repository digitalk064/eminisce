from django.forms import ModelForm
from django.forms import inlineformset_factory

from .models.book import Book, Author, BookBarcode
from .models.libraryuser import LibraryUser
from .models.loans import Loan

from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

from datetime import datetime,timedelta,time
from django.utils import timezone

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

class LoanForm(ModelForm):

    start_date = forms.DateTimeField(widget=DateTimePickerInput(
            format='%d/%m/%Y %H:%M',
            attrs={'width':'50%',},
            options= {
                'minDate': datetime.today().strftime('%Y-%m-%d 00:00:00'),
            }
        ), 
        help_text = "The start date of the loan.", label = "Start Date", 
        initial=timezone.now(),
        input_formats=("%d/%m/%Y %H:%M",),
    )

    due_date = forms.DateTimeField(widget=DateTimePickerInput(
            format='%d/%m/%Y %H:%M',
            attrs={'width':'50%',},
            options= {
                'minDate': datetime.today().strftime('%Y-%m-%d 00:00:00'),
            }
        ), 
        help_text = "The due date of the loan.", label = "Due Date", 
        initial = timezone.now() + timedelta(days=Loan.DEFAULT_LOAN_DAYS),
        input_formats=("%d/%m/%Y %H:%M",),
    )

    class Meta:
        model = Loan
        fields = "__all__"
        exclude = ['status', 'return_date']