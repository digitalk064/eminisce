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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

import eminisce.controllers.common
from eminisce.controllers.user import browse_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",  eminisce.controllers.common.index, name="index"),
    path("admin/", admin.site.urls, name = "admin"),
    
    path("login/", auth_views.LoginView.as_view(template_name ="login.html"), name = "login"),
    #Since a registering page shouldnt exist, we just redirect it to the login page
    path("register/", auth_views.LoginView.as_view(template_name ="login.html"), name = "register"),
    path("logout/", auth_views.LogoutView.as_view(template_name ="logout.html"), name = "logout"),

    path("browse/", browse_catalog.browse, name = "browse_catalog"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)