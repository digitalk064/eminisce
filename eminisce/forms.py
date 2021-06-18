from django.forms import ModelForm
from django.forms import inlineformset_factory

from .models.book import Book, Author, BookBarcode
from .models.libraryuser import LibraryUser
from .models.loans import Loan

from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

from datetime import datetime,timedelta,time
from django.utils import timezone
from django.conf import settings

timezone.activate(settings.TIME_ZONE)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

#AuthorFormSet = inlineformset_factory(Author, Book, form=AuthorForm, can_delete=False)

class BinaryFileInput(forms.ClearableFileInput):

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value)

    def format_value(self, value):
        """Format the size of the value in the db.

        We can't render it's name or url, but we'd like to give some information
        as to wether this file is not empty/corrupt.
        """
        if self.is_initial(value):
            return f'{len(value)} bytes'


    def value_from_datadict(self, data, files, name):
        """Return the file contents so they can be put in the db."""
        upload = super().value_from_datadict(data, files, name)
        if upload:
            return upload.read()

class LibraryUserForm(ModelForm):

    idnum = forms.CharField(label="Identification Number", help_text="Can be Student ID or Employee ID, used for logging in.")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LibraryUser
        fields = ['idnum', 'password', 'fullname', 'user_type', 'fingerprint']
        exclude = ['status', 'user']
        widgets = {
            'fingerprint': BinaryFileInput(),
        }
        help_texts = {
            'fingerprint': '(Optional) Upload fingerprint file generated from the fingerprint reader.',
        }

class LibraryUserEditForm(ModelForm):

    idnum = forms.CharField(label="Identification Number", help_text="Can be Student ID or Employee ID, used for logging in.")

    class Meta:
        model = LibraryUser
        fields = ['idnum', 'fullname', 'user_type', 'status', 'fingerprint']
        exclude = ['user']
        widgets = {
            'fingerprint': BinaryFileInput(),
        }
        help_texts = {
            'fingerprint': '(Optional) Upload fingerprint file generated from the fingerprint reader.',
        }

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

class LoanEditForm(ModelForm):

    due_date = forms.DateTimeField(widget=DateTimePickerInput(
            format='%d/%m/%Y %H:%M',
            attrs={'width':'50%',},
            options= {
                'minDate': datetime.today().strftime('%Y-%m-%d 00:00:00'),
            }
        ), 
        help_text = "The new due date of the loan.", label = "New due date", 
        input_formats=("%d/%m/%Y %H:%M",),
    )

    class Meta:
        model = Loan
        fields = ('due_date',)