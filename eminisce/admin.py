from django.contrib import admin
from .models.book import Book, Author, BookBarcode

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.html import format_html


#Custom Admin Models
class BookAdmin(admin.ModelAdmin):
    change_form_template = 'admin/room_change_approve.html'
    exclude = ('created_by','status')
    search_fields = ('name','location')
    list_filter = ('status',)