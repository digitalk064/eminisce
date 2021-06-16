from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.loans import Loan

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mark_loan_returned(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return HttpResponse("Error: Cannot find loan")
    
    loan.set_returned()
    messages.success(request, "Successfully updated loan\'s status.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    