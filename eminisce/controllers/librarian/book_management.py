from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from django.contrib.auth.models import User

from django_tables2 import RequestConfig
from django.db.models import Q

from .tables import BookTable

from django.contrib.admin.views.decorators import staff_member_required

import requests

@staff_member_required
def index(request):
    context = {"books_active" : "active"} #change navbar active element

    keywords = request.GET.get('keywords','')
    if request.method == "GET":
        context['keywords'] = keywords
    search_by = request.GET.get('search_by', '')

    if search_by == "title":
        books = Book.objects.filter(Q(title__icontains=keywords))
    elif search_by == "author":
        books = Book.objects.filter(Q(authors__icontains=keywords))
    elif search_by == "barcode":
        books = Book.objects.filter(Q(barcode__icontains=keywords))
    else:
        books = Book.objects.all()

    table = BookTable(books, order_by="title")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context['table'] = table

    return render(request, "librarian/book_management.html", context)
