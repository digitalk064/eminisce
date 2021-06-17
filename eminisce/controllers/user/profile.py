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

from eminisce.models.loans import LibraryUser

import requests

@login_required
def index(request):
    context = {"home_active" : "active"} #change navbar active element

    context['blacklisted'] = True if request.user.libraryuser.status == LibraryUser.Status.CANNOTBORROW else False

    return render(request, "user/profile.html", context)