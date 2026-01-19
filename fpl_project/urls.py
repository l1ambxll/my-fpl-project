"""
URL configuration for fpl_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from fpl_project import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    
    # Accounts app URLs
    path("", include("accounts.urls")),

    # Domain apps
    path('players/', include('players.urls')),
    path('teams/', include('teams.urls')),
    path('leagues/', include('leagues.urls')),
]
