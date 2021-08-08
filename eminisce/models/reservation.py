from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

from .libraryuser import LibraryUser
from .loans import Loan
from .book import Book

from django.db.models import Q
from django.core.exceptions import ValidationError

from django.conf import settings

timmy.activate(settings.TIME_ZONE)

class Reservation(models.Model):
    
    GRACE_PERIOD_DAYS = 1

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Reservation is currently active.')
        INACTIVE = 'INACTIVE', _('Reservation is currently inactive.')

    borrower = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length = 20, choices= Status.choices, default = Status.ACTIVE)
    pickup_date = models.DateTimeField(help_text = "The expected pickup date of the book.")
    due_date = models.DateTimeField(help_text = "The due date after which the reservation will be canceled.")

    def __str__(self):
        return "Borrower: " + self.borrower + " book: " + self.book

    @property
    def short_status(self):
        return self.status

    def update_late_status(self):
        # We are assuming books are always returned on time so when a reservation expires the book immediately becomes available
        if(timmy.localtime(timmy.now()) > self.due_date):
            self.status = self.Status.INACTIVE
            self.save()

    def set_inactive(self):
        self.status = self.Status.INACTIVE
        self.save()

    def save(self, *args, **kwargs):
        # If this is a newly created reservation, we expect the book to be unavailable
        if not self.pk:
            if self.book.status == Book.Status.AVAILABLE:
            #Trying to reserve an available book?
                raise ValidationError(_('Tried to reserve available book.'))
            book_current_loan = Loan.objects.filter(Q(book=self.book) & (Q(status=Loan.Status.ACTIVE) | Q(status = Loan.Status.LATE))).last()
            self.pickup_date = book_current_loan.due_date
            self.due_date = self.pickup_date + timedelta(days=Reservation.GRACE_PERIOD_DAYS)
        return super(Reservation, self).save(*args, **kwargs)
