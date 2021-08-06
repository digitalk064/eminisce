from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.forms import LibraryUserEditForm
from eminisce.models.libraryuser import LibraryUser
from django.contrib.auth.models import User

from PIL import Image
import io

@staff_member_required
def edit_user(request, edit_id):

    context = {"accounts_active" : "active"} #change navbar active element
    try:
        libraryuser = LibraryUser.objects.get(id=edit_id)
        user = libraryuser.user
    except LibraryUser.DoesNotExist:
        return HttpResponse("Error: Cannot find user")
        
    context['user_fullname'] = libraryuser.fullname

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
        form = LibraryUserEditForm(request.POST, request.FILES, instance=libraryuser)
        
        if form.is_valid():
            #Get the ID
            idnum = form.cleaned_data['idnum']
            # If the ID has changed, check if there's another account already using the new ID:
            # Not optimal but we do not expect IDs to be changed that much
            if idnum != user.username and User.objects.filter(username=idnum).exists():
                # If another account already uses the new ID, error out
                form.add_error('idnum', 'Another account with this ID already exists!')
            else:
                #Update the username (ID) of the main user
                user.username = idnum
                user.save()
                #Save the edit
                libraryuser = form.save()

                # If fingerprint or face images were uploaded, save the processed files to the database
                if processed_fingerprint:
                    libraryuser.fingerprint = processed_fingerprint
                if processed_face:
                    libraryuser.face_front = processed_face
                libraryuser.save()
                
                #Alert the user of the success
                messages.success(request, 'Library user successfully updated.')
                return redirect(request.META['HTTP_REFERER'])
    else:                
        form = LibraryUserEditForm(instance=libraryuser, initial={"idnum":user.username})
    context['form'] = form

    return render(request, "librarian/edit_user.html", context)

def post_process_img(original):
    #from base64 import b64encode
    #print(b64encode(original).decode('utf8'))
    #print(str.encode(b64encode(original).decode('utf8')))
    #print(original)
    # Open image with Pillow
    processed = Image.open(io.BytesIO(original))
    processed.thumbnail((320, 320), Image.ANTIALIAS)
    # Convert to bytes again to save to database
    img_byte_arr = io.BytesIO()
    processed.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr