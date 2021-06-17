from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from eminisce.models.book import Book

from django.conf import settings

@login_required
def view_book(request, barcode):
    context = {"browse_active" : "active"} #change navbar active element
    # Get book's details
    try:
        book = Book.objects.get(barcode=barcode)
        context["book"] = book
        if(book.status == Book.Status.AVAILABLE):
            context["available"] = True
    except Book.DoesNotExist:
        messages.error(request, "Cannot find book with specified barcode!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "books/book_desc.html", context)