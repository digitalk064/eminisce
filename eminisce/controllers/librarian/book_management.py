from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from django.contrib.auth.models import User

from django_tables2 import RequestConfig

from .tables import BookTable

from django.contrib.admin.views.decorators import staff_member_required

import requests

@staff_member_required
def index(request):
    context = {"books_active" : "active"} #change navbar active element

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')

    table = BookTable(Book.objects.filter(title__icontains=context['keywords']))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context['table'] = table

    return render(request, "librarian/book_management.html", context)
