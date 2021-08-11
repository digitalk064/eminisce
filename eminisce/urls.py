"""eminisce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

import eminisce.controllers.common
from eminisce.controllers.user import browse_catalog, view_book, profile, pay_fines, reserve_book, extend_duedate
from eminisce.controllers.librarian import create_user, user_management, delete_user, edit_user
from eminisce.controllers.librarian import book_management, create_book, delete_book, edit_book
from eminisce.controllers.librarian import loan_management, create_loan, mark_loan_returned, edit_loan
from eminisce.controllers.librarian import fine_management, create_fine, mark_fine_paid, edit_fine

urlpatterns = [
    # Admin places
    path('admin/', admin.site.urls),
    path("",  eminisce.controllers.common.index, name="index"),
    path("admin/", admin.site.urls, name = "admin"),
    
    # Common places
    path("login/", auth_views.LoginView.as_view(template_name ="login.html"), name = "login"),
    #Since a registering page shouldnt exist, we just redirect it to the login page
    path("register/", auth_views.LoginView.as_view(template_name ="login.html"), name = "register"),
    path("logout/", auth_views.LogoutView.as_view(template_name ="logout.html"), name = "logout"),

    # User places
    path("browse/", browse_catalog.browse, name = "browse_catalog"),
    path("profile/", profile.index, name = "user_profile"),
    path("pay_fines/", pay_fines.pay_fines, name = "pay_fines"),

    # View book description
    path("browse/view_book/<str:barcode>",  view_book.view_book, name = "view_book_desc"),

    # Reserve book
    path("reserve_book/",  reserve_book.reserve_book, name = "reserve_book"),
    # Extend due date
    path("extend_duedate/<int:loan_id>",  extend_duedate.extend_duedate, name = "extend_duedate"),

    # Librarian places
    # User Management
    path("librarian/accounts", user_management.index, name = "librarian_manage_user"),
    path("librarian/createuser", create_user.create_user, name = "librarian_create_user"),
    # Reverses (for actions on objects)
    path('librarian/accounts/edit_user/<int:edit_id>', edit_user.edit_user, name='edit_user'),
    path('librarian/accounts/delete_user/<int:del_id>', delete_user.delete_user, name='delete_user'),

    # Book Management
    path("librarian/books", book_management.index, name = "librarian_manage_book"),
    path("librarian/createbook", create_book.create_book, name = "librarian_create_book"),
    path('librarian/books/edit_book/<int:edit_id>', edit_book.edit_book, name='edit_book'),
    path('librarian/books/delete_book/<int:del_id>', delete_book.delete_book, name='delete_book'),

    # Loan Management
    path("librarian/loans", loan_management.index, name = "librarian_manage_loan"),
    path("librarian/createloan", create_loan.create_loan, name = "librarian_create_loan"),
    path('librarian/loans/mark_loan_returned/<int:loan_id>', mark_loan_returned.mark_loan_returned, name='mark_loan_returned'),
    path('librarian/loans/edit_loan/<int:loan_id>', edit_loan.edit_loan, name='edit_loan'),
    #path('librarian/books/delete_book/<int:del_id>', delete_book.delete_book, name='delete_book'),

    # Fine Management
    path("librarian/fines", fine_management.index, name = "librarian_manage_fine"),
    path("librarian/createfine", create_fine.create_fine, name = "librarian_create_fine"),
    path('librarian/fines/mark_fine_paid/<int:fine_id>', mark_fine_paid.mark_fine_paid, name='mark_fine_paid'),
    path('librarian/fines/edit_fine/<int:fine_id>', edit_fine.edit_fine, name='edit_fine'),

    #REST API
    path('api/', include('eminisce.api.api_urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)