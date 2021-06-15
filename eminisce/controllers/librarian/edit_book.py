from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.forms import BookForm
from eminisce.models.book import Book
from django.contrib.auth.models import User

@staff_member_required
def edit_book(request, edit_id):

    context = {"books_active" : "active"} #change navbar active element
    try:
        book = Book.objects.get(id=edit_id)
    except Book.DoesNotExist:
        return HttpResponse("Error: Cannot find book")
        
    context['book_barcode'] = book.barcode

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = BookForm(request.POST, request.FILES, instance=book)
        #Check if valid first
        if form.is_valid():
            #Save the edit
            form.save()
            #Alert the user of the success
            messages.success(request, 'Book successfully updated.')
            return redirect('librarian_manage_book')
    else:                
        form = BookForm(instance=book)
    context['form'] = form

    return render(request, "librarian/edit_book.html", context)