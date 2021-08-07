from django.shortcuts import render, redirect

from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.models.fines import Fine

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mark_fine_paid(request, fine_id):
    try:
        fine = Fine.objects.get(id=fine_id)
    except Fine.DoesNotExist:
        return HttpResponse("Error: Cannot find fine")
    
    fine.set_paid()
    messages.success(request, "Successfully updated fine\'s status.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    