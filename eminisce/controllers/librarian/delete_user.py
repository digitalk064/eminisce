from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def delete_user(request, del_id):
    User.objects.filter(id=del_id).delete()
    messages.success(request, 'Library user successfully deleted.')
    return redirect('librarian_manage_user')