from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db.models import Q

from datetime import datetime, time, timedelta
from django.utils import timezone as timmy #Avoid naming conflict
from pytz import timezone
from django.conf import settings

from eminisce.models.book import Book

import requests

@login_required
def browse(request):
    context = {"browse_active" : "active"} #change navbar active element

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
        
    if 'available' in request.GET:
        print("AVAILABLE ONLY")
        books = books.filter(status=Book.Status.AVAILABLE)
    
    for book in books:
        book.available = True if book.status == Book.Status.AVAILABLE else False
    
    context['books'] = list(books)

    return render(request, "user/browse.html", context)