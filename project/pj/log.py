import datetime
import hashlib
import time

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from votedb.models import user, login_log


def log_url(request):
    if request.session.get('is_login', False):
        username = request.session['username']
        try:
            user_ite = user.objects.get(name = username)
            if user_ite.authority < 2:
                return HttpResponse("需要管理员权限")
            else:
                context = {}
                loglist = login_log.objects.all()
                context['loglist'] = loglist
                return render(request, 'log.html', context)
        except ObjectDoesNotExist:
            return HttpResponse("用户不存在")
    else:
        return HttpResponse("请先登录")
