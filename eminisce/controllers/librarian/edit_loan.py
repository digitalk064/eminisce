from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from eminisce.forms import LoanEditForm
from eminisce.models.loans import Loan
from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone

@staff_member_required
def edit_loan(request, loan_id):
    timezone.activate(settings.TIME_ZONE)
    context = {"loans_active" : "active"} #change navbar active element
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return HttpResponse("Error: Cannot find loan")
        
    context['loan_id'] = loan.pk

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = LoanEditForm(request.POST, instance=loan)
        #Check if valid first
        if form.is_valid():
            #Save the edit
            form.save()
            #Alert the user of the success
            messages.success(request, 'Loan successfully updated.')
            return redirect('librarian_manage_loan')
    else:                
        form = LoanEditForm(instance=loan)
    context['form'] = form

    return render(request, "librarian/edit_loan.html", context)