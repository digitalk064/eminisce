from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone as timmy #Avoid naming conflict
from datetime import datetime,timedelta,time
import pytz

from pytz import timezone
from django.utils.html import mark_safe

from base64 import b64decode, b64encode

# Since there is a weird bug with the built-in BinaryField where it tries to encode
# to base64 before putting in the database but it encodes the filename not the actual file bytes
# for some reason, and the filename being something random can make the encoding fail
# we just force it to encode a string that will not fail
# since we will replace the face_front value with the correctly processed image anyway in edit_user.py
class FixedBinaryInputField(models.BinaryField):
    def to_python(self, value):
        # If it's a string, it should be base64-encoded data
        if isinstance(value, str):
            return memoryview(b64decode("".encode('utf-8')))
        return value

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
    user_type = models.CharField(max_length = 30, choices= UserType.choices, default = UserType.STUDENT, help_text="Note: Staff member does NOT mean the account has access privileges as a librarian, it means the account belongs to a faculty member, not a student.")

    #Biometrics data
    fingerprint = FixedBinaryInputField(null = True, blank=True, editable=True, default=None)
    face_front = FixedBinaryInputField(null = True, blank=True, editable=True, verbose_name="Face recognition", default=None)
    # Is it worth saving 3 photos of each person?
    face_leftside = FixedBinaryInputField(null = True, blank=True, editable=True, default=None)
    face_rightside = FixedBinaryInputField(null = True, blank=True, editable=True, default=None)

    def face_image_display(self):
        if self.face_front is None or self.face_front == b'':
            return "This user currently does not have a facial recognition photo uploaded."
        return mark_safe('<img src = "data: image/png; base64, {}" height="320">'.format(
            b64encode(self.face_front).decode('utf8')
        ))

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
    def has_face(self):
        if not self.face_front:
            return False
        else:
            return True
    @property
    def can_borrow(self):
        if self.status == "CAN BORROW":
            return True
        else:
            return False
