"""codeforces_crawler URL Configuration

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
from django.urls import path,include
from .views import IndexView

from . import views, settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView,name = 'index'),
    path('accounts/',include('accounts.urls')),
    path('contests/',include('contests.urls')),
    path('friendship/', include('friendship.urls')),
    path('solutions/',include('solutions.urls')),
    path('forum/',include('forum.urls')),
    path('charts/',include('charts.urls')),
    path('team/',views.Team,name = 'Team'),
    # Note that you do not necessarily need the URLs provided by django.contrib.auth.urls.
    # Instead of the URLs login, logout, and password_change (among others),
    # you can use the URLs provided by allauth: account_login, account_logout, account_set_password…
    path('accounts/', include('allauth.urls')),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
