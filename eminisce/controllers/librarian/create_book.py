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

from eminisce.forms import BookForm
from eminisce.models.book import Book
from django.contrib.auth.models import User

import requests

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def create_book(request):
    context = {"books_active" : "active"} #change navbar active element

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = BookForm(request.POST, request.FILES)
        #Check if valid first
        if form.is_valid():
            form.save()
            messages.success(request, 'Book successfully added to catalog.')
            return redirect('librarian_manage_book')
    else:
        form = BookForm()
    context['form'] = form

    return render(request, "librarian/create_book.html", context)