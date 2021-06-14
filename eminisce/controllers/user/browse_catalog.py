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

import requests

@login_required
def browse(request):
    context = {"browse_active" : "active"} #change navbar active element

    if request.method == "GET":
        context['keywords'] = request.GET.get('keywords','')

    return render(request, "user/browse.html", context)