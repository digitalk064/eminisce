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

from eminisce.forms import FineForm
from eminisce.models.book import Book
from django.contrib.auth.models import User

import requests

from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
from django.utils import timezone

@staff_member_required
def create_fine (request):
    timezone.activate(settings.TIME_ZONE)

    context = {"fines_active" : "active"} #change navbar active element

    #Handle submitting form
    if request.method == "POST":
        #Get the submitted form
        form = FineForm(request.POST)
        #Check if valid first
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully created fine entry.')
            return redirect('librarian_manage_fine')
    else:
        form = FineForm()
    context['form'] = form

    return render(request, "librarian/create_fine.html", context)