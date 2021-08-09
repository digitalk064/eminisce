from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

from .libraryuser import LibraryUser
from .book import Book

from django.conf import settings

timmy.activate(settings.TIME_ZONE)

class Loan(models.Model):
    
    DEFAULT_LOAN_DAYS = 21


    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Loan is currently active.')
        RETURNED = 'RETURNED', _('Loan is finished, book returned.')
        LATE = 'LATE', _('Loan not finished, user is late on returning book.')
        RETURNED_LATE = 'RETURNED LATE', _('Loan finished, but book was returned past due.')

    def due_date_field():
        datetime.now()+timedelta(days=Loan.DEFAULT_LOAN_DAYS)

    borrower = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length = 20, choices= Status.choices, default = Status.ACTIVE)
    start_date = models.DateTimeField(default=datetime.now, help_text = "The start date of the loan.")
    due_date = models.DateTimeField(default= due_date_field, help_text = "The due date of the loan.")
    return_date = models.DateTimeField(help_text = "The actual date the book was returned and the loan finishes.", null=True)

    def __str__(self):
        return f"Borrower: {self.borrower} book: {self.book}"

    @property
    def short_status(self):
        return self.status

    def update_late_status(self):
        if(timmy.localtime(timmy.now()) > self.due_date):
            self.status = self.Status.LATE
            self.save()

    def set_returned(self):
        # Assign return date
        self.return_date = timmy.now()
        # Update status
        if(self.return_date < self.due_date):
            self.status = self.Status.RETURNED
        else:
            self.status = self.Status.RETURNED_LATE
            # Do something?
        self.save()

    def save(self, *args, **kwargs):
        # If this is a newly created loan, we expect the book to be unavailable
        if not self.pk:
            self.book.set_unavailable()
            # Check if due date is set, if it is not it is most likely an API call to new_loan, in that case set the due_date ourselves
            if self.due_date is None:
                # self.due_date = self.due_date_field() WHY DOESN'T THIS WORK?!?!?
                self.due_date = datetime.now()+timedelta(days=Loan.DEFAULT_LOAN_DAYS)
        else:
            # If the new status is returned, make the book available again and set return_date field
            if self.status == self.Status.RETURNED or self.status == self.Status.RETURNED_LATE:
                # Set the book to available again
                self.book.set_available()
                # Set the return date
                # self.return_date = timmy.now()
        return super(Loan, self).save(*args, **kwargs)