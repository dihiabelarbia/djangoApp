"""Django_v URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path

from .views import home, logpaths,upload, search, scripts_run, scripts_exec

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path("logpaths", logpaths),
    path("search/", upload),
    path("search/find", search),
    path("tests", scripts_run),
    path("<path:path>",scripts_exec, name='scripts_exec')
]