from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

class Author(models.Model):
   name = models.CharField(max_length=100)

class BookBarcode(models.Model):
   barcode = models.CharField(max_length=10)

class Book(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', _('Available')
        UNAVAILABLE = 'UNAVAILABLE', _('Unavailable')
        TAKENOFF = 'TAKEN OFF', _('Taken off from the library')

    title = models.CharField(max_length = 60)
    authors = models.CharField(max_length=100, help_text="Separated by commas.")
    description = models.TextField()
    cover = models.ImageField(null=True, blank=True, upload_to ='book_covers/')
    status = models.CharField(max_length = 30, choices= Status.choices, default = Status.AVAILABLE)
    barcode = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "Book: " + self.title