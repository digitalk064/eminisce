from eminisce.models.loans import Loan
from django.utils import timezone as timmy

def auto_update_loans():
    print("Hello")
    loan = Loan.objects.last()
    loan.return_date = timmy.now()
    loan.save()
