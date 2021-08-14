from django.shortcuts import render, redirect

from eminisce.models.libraryuser import LibraryUser
from eminisce.models.fines import Fine

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

def pay_fines(request):

    # PLEASE PUT YOUR OWN PAYMENT PROCESSING HERE
    
    # Simulate payment successful and set all fines to paid
    fines = Fine.objects.filter(borrower=request.user.libraryuser).filter(status=Fine.Status.UNPAID)
    for fine in fines:
        fine.set_paid()
    messages.success(request, "Transaction successful. You have paid all your fines.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    