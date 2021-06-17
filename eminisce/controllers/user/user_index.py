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

from eminisce.models.loans import Loan
from eminisce.models.book import Book

import requests

@login_required
def index(request):
    context = {"home_active" : "active"} #change navbar active element

    # Get all the user's active loans
    loans = Loan.objects.filter(Q(borrower=request.user.libraryuser) & (Q(status=Loan.Status.ACTIVE) | Q(status = Loan.Status.LATE))).order_by("-start_date")
    for loan in loans:
        loan.extend_button_status = "disabled" if loan.status != Loan.Status.ACTIVE else ""
        loan.due_in = (loan.due_date - timmy.now()).days
        # Check if overdue
        if loan.due_in < 0:
            loan.overdue = True
            loan.due_in = abs(loan.due_in)
            loan.extend_button_status = "disabled"

    # Get all the user's past loans
    past_loans = Loan.objects.filter(Q(borrower=request.user.libraryuser) & (Q(status=Loan.Status.RETURNED) | Q(status = Loan.Status.RETURNED_LATE))).order_by("-return_date")
    past_loans = list(past_loans)

    loans = list(loans)
    context["loans"] = loans
    context["past_loans"] = past_loans


    return render(request, "user/index.html", context)