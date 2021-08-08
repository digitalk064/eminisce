from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.reservation import Reservation

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

def reserve_book(request):
    if request.method == 'POST':
        barcode = request.POST.get("barcode", None)
        if barcode:
            if request.user.libraryuser is None:
                messages.error(request, "No book barcode provided.")
            else:
                try:
                    reservation = Reservation.objects.create(book=Book.objects.get(barcode=barcode), borrower=request.user.libraryuser)
                    messages.success(request, f'Successfully reserved this book. Expected availability date is {reservation.pickup_date}, please pick up book at the latest {reservation.due_date}')
                except Book.DoesNotExist:
                    messages.error(request, "Cannot find this book in database.")
                except ValidationError as e:
                    messages.error(request, e.message)
        else:
            messages.error(request, "No book barcode provided.")
        

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    