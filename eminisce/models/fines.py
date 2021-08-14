from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

from .libraryuser import LibraryUser
from .book import Book

from django.core.validators import MinValueValidator

class Fine(models.Model):
    
    class Status(models.TextChoices):
        PAID = 'PAID', _('Fine has been settled.')
        UNPAID = 'UNPAID', _('Fine is not yet paid.')

    borrower = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=False, help_text="Amount in SGD. Up to 2 decimal places.", verbose_name="Amount", validators=[MinValueValidator(0.01)])
    reason = models.CharField(blank=True, null=True, max_length=200, help_text="Reason for the fine.", verbose_name = "Reason")
    status = models.CharField(max_length = 20, choices= Status.choices, default = Status.UNPAID)
    issue_date = models.DateTimeField(default=datetime.now, help_text = "The issue date of the loan.")
    paid_date = models.DateTimeField(help_text = "The date the user has paid for this fine.", null=True)

    def __str__(self):
        return f"User: {self.borrower}. Amount: {self.amount} SGD"

    @property
    def short_status(self):
        return self.status

    def set_paid(self):
        # Assign paid date
        self.paid_date = timmy.now()
        self.status = self.Status.PAID
        self.save()