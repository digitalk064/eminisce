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

from .user import user_index

import requests

@login_required
def index(request):
    #If user is staff, take user to admin page right away
    if request.user.is_staff:
        context = {"home_active" : "active"} #change navbar active element

        return render(request, "librarian/index.html", context)
    # If the user is not a staff, take user to the normal library user page
    else:

        return user_index.index(request)