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

from eminisce.forms import LibraryUserForm
from eminisce.models.libraryuser import LibraryUser
from django.contrib.auth.models import User

import requests

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def create_user(request):
    context = {"accounts_active" : "active"} #change navbar active element

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = LibraryUserForm(request.POST, request.FILES)
        #Check if valid first
        if form.is_valid():
            #Get the ID
            idnum = form.cleaned_data['idnum']
            #Check if there's another account already using the ID:
            if User.objects.filter(username=idnum).exists():
                form.add_error('idnum', 'An account with this ID already exists!')
            #If not, we can proceed with creating an account
            else:
                new_user = User.objects.create_user(username = idnum, password = form.cleaned_data['password'])
                #Prepare to create a new library user object but don't save it yet
                _libraryuser = form.save(commit=False)
                #Assign the user object to the library user foreign key
                _libraryuser.user = new_user
                #Save it
                _libraryuser.save()
                #Alert the user of the success
                messages.success(request, 'Library user successfully created.')
                return redirect('librarian_manage_user')
    else:
        form = LibraryUserForm()
    context['form'] = form

    return render(request, "librarian/create_user.html", context)