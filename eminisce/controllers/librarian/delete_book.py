from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.models.book import Book

@staff_member_required
def delete_book(request, del_id):
    Book.objects.filter(id=del_id).delete()
    messages.success(request, 'Book successfully removed.')
    return redirect('librarian_manage_book')