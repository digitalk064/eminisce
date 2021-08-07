from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.fines import Fine
from django.contrib.auth.models import User
from django.db.models import Q

from django_tables2 import RequestConfig

from .tables import FineTable

from django.contrib.admin.views.decorators import staff_member_required

import requests

@staff_member_required
def index(request):
    context = {"fines_active" : "active"} #change navbar active element

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')

    table = FineTable(Fine.objects.filter(Q(borrower__fullname__icontains=context['keywords']) | Q(reason__icontains=context['keywords'])), order_by="-issue_date")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context['table'] = table

    return render(request, "librarian/fine_management.html", context)
