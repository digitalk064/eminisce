from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.loans import Loan
from django.contrib.auth.models import User
from django.db.models import Q

from django_tables2 import RequestConfig

from .tables import LoanTable

from django.contrib.admin.views.decorators import staff_member_required

import requests

@staff_member_required
def index(request):
    context = {"loans_active" : "active"} #change navbar active element

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')

    table = LoanTable(Loan.objects.filter(Q(borrower__fullname__icontains=context['keywords']) | Q(book__barcode__icontains=context['keywords'])), order_by="-start_date")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context['table'] = table

    return render(request, "librarian/loan_management.html", context)
