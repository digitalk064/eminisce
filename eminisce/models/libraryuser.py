from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone

class LibraryUser(models.Model):

    class Status(models.TextChoices):
        CANBORROW = 'CAN BORROW', _('User is allowed to borrow books')
        CANNOTBORROW = 'CANNOT BORROW', _('User is not allowed to borrow books')

    class UserType(models.TextChoices):
        STUDENT = 'STUDENT', _('User is a student enrolled in the institution.')
        CORP = 'CORPORATE MEMBER', _('User is a staff member in the institution')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #idnum = models.CharField(max_length=30, help_text="Identification number of the library user. Copied over from the username of the user", editable=False)
    fullname = models.CharField(max_length=100, help_text="Full name of the library user.", verbose_name = "Full name")
    status = models.CharField(max_length = 30, choices= Status.choices, default = Status.CANBORROW)
    user_type = models.CharField(max_length = 30, choices= UserType.choices, default = UserType.STUDENT)
    fingerprint = models.BinaryField(null = True, blank=True, editable=True)

    def __str__(self):
        return self.user.username + " " + self.fullname

    @property
    def short_user_type(self):
        return self.user_type
    @property
    def has_fingerprint(self):
        if not self.fingerprint:
            return False
        else:
            return True
    @property
    def can_borrow(self):
        if self.status == "CAN BORROW":
            return True
        else:
            return False