from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.loans import Loan
from eminisce.forms import LoanFilterForm
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime

from django_tables2 import RequestConfig

from .tables import LoanTable

from django.contrib.admin.views.decorators import staff_member_required

import requests

@staff_member_required
def index(request):
    context = {"loans_active" : "active"} #change navbar active element

    f_start_date = None
    f_return_date = None

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')
        context['filter'] = request.GET.get('filter','')
        f_start_date = request.GET.get('start_date', '')
        f_return_date = request.GET.get('return_date', '')

        context['filter_form'] = LoanFilterForm()

    loans = Loan.objects.filter(Q(borrower__fullname__icontains=context['keywords']) | Q(book__barcode__icontains=context['keywords'])).filter(status__icontains=context['filter'])
    if(f_start_date != ''):
        f_start_date = datetime.strptime(f_start_date, '%m/%d/%Y')
        loans = loans.filter(start_date__date=f_start_date)
    if(f_return_date != ''):
        f_return_date = datetime.strptime(f_return_date, '%m/%d/%Y')
        loans = loans.filter(return_date__date=f_return_date)

    table = LoanTable(loans, order_by="-start_date")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context['table'] = table

    return render(request, "librarian/loan_management.html", context)
