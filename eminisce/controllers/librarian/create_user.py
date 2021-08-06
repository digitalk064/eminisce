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

from PIL import Image
import io

@staff_member_required
def create_user(request):
    context = {"accounts_active" : "active"} #change navbar active element

    #Handle submitting form
    if request.method == "POST":

         # First, if fingerprint or face images were uploaded, we have to process them
        processed_fingerprint = None
        processed_face = None

        if not request.FILES.get('fingerprint', None):
            print("No fingerprint uploaded")
        else:
            processed_fingerprint = request.FILES.get('fingerprint').read() # Keep fingerprint file raw

        if not request.FILES.get('face_front', None):
            print("No face uploaded")
        else:
            processed_face = post_process_img(request.FILES.get('face_front').read()) # Resize the image to save storage space
        
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

                # If fingerprint or face images were uploaded, save the processed files to the database
                if processed_fingerprint:
                    _libraryuser.fingerprint = processed_fingerprint
                if processed_face:
                    _libraryuser.face_front = processed_face

                #Save it
                _libraryuser.save()
                #Alert the user of the success
                messages.success(request, 'Library user successfully created.')
                return redirect('librarian_manage_user')
    else:
        form = LibraryUserForm()
    context['form'] = form

    return render(request, "librarian/create_user.html", context)

def post_process_img(original):
    # Open image with Pillow
    processed = Image.open(io.BytesIO(original))
    processed.thumbnail((160, 160), Image.ANTIALIAS)
    # Convert to bytes again to save to database
    img_byte_arr = io.BytesIO()
    processed.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr