from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.forms import LibraryUserEditForm
from eminisce.models.libraryuser import LibraryUser
from django.contrib.auth.models import User

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
        #Get the submitted form
        form = LibraryUserEditForm(request.POST, instance=libraryuser)
        #Check if valid first
        if form.is_valid():
            #Get the ID
            idnum = form.cleaned_data['idnum']
            #Check if there's another account already using the ID:
            if idnum != user.username and User.objects.filter(username=idnum).exists():
                form.add_error('idnum', 'Another account with this ID already exists!')
            #If not, we can proceed with creating an account
            else:
                #Update the username (ID) of the main user
                user.username = idnum
                user.save()
                #Save the edit
                form.save()
                #Alert the user of the success
                messages.success(request, 'Library user successfully updated.')
                return redirect('librarian_manage_user')
    else:                
        form = LibraryUserEditForm(instance=libraryuser, initial={"idnum":user.username})
    context['form'] = form

    return render(request, "librarian/edit_user.html", context)