from django.shortcuts import render, redirect

from eminisce.models.libraryuser import LibraryUser
from eminisce.models.loans import Loan

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

def extend_duedate(request, loan_id):
    loan = Loan.objects.get(id = loan_id)
    loan.extend_duedate()
    
    messages.success(request, 'You have successfully requested to extend the due date for this book. Your due date has been pushed back by 7 days.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    