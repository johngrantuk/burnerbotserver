"""burnerbotserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.feed, name='feed'),
    # url(r'^userInfo/$', views.userInfo),
    url(r'^userInfo/(?P<username>[-\w]+)/(?P<hash>[-\w]+)/$', views.userInfo),
    url(r'^userAddress/(?P<username>[-\w]+)/$', views.userAddress),
    url(r'^register/$', views.register, name='register'),
    path('admin/', admin.site.urls),
]

# Burn
# Remove user
# change emoji
