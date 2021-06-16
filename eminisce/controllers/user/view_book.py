from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.conf import settings

@login_required
def view_book(request, book_id):
    context = {"browse_active" : "active"} #change navbar active element

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')

    return render(request, "books/book_desc.html", context)