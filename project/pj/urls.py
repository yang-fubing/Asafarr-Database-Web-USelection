"""pj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from pj.db_init import init
from pj.candidate import candidate_url
from pj.debates import debates_url
from pj.log import log_url
from pj.tweet import tweet_url
from pj.votes import votes_url
from pj.welcome import welcome_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('init/', init),
    path('candidate/', candidate_url),
    path('tweet/', tweet_url),
    path('votes/', votes_url),
    path('debates/', debates_url),
    path('log/', log_url),
    path('', welcome_url)
]

urlpatterns += static('/candidate/', document_root = settings.MEDIA_ROOT)
urlpatterns += static('/tweet/', document_root = settings.MEDIA_ROOT)
urlpatterns += static('/votes/', document_root = settings.MEDIA_ROOT)
urlpatterns += static('/debates/', document_root = settings.MEDIA_ROOT)
urlpatterns += static('/', document_root = settings.MEDIA_ROOT)
