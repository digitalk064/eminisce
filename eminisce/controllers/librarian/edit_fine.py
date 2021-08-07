from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.forms import FineEditForm
from eminisce.models.fines import Fine
from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone

@staff_member_required
def edit_fine(request, fine_id):
    timezone.activate(settings.TIME_ZONE)
    context = {"fines_active" : "active"} #change navbar active element
    try:
        fine = Fine.objects.get(id=fine_id)
    except Fine.DoesNotExist:
        return HttpResponse("Error: Cannot find fine")
        
    context['fine_id'] = fine.pk

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = FineEditForm(request.POST, instance=fine)
        #Check if valid first
        if form.is_valid():
            #Save the edit
            form.save()
            #Alert the user of the success
            messages.success(request, 'Fine successfully updated.')
            return redirect('librarian_manage_fine')
    else:                
        form = FineEditForm(instance=fine)
    context['form'] = form

    return render(request, "librarian/edit_fine.html", context)