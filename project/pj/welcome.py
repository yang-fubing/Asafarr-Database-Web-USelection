import datetime
import hashlib
import time

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from votedb.models import user, login_log, state_vote, state_info, candidate


def welcome_url(request):
    context = {}
    message = ""
    if request.POST:
        if "login" in request.POST:
            if request.session.get('is_login', False):
                message = "login ed!"
            else:
                try:
                    user_std = user.objects.get(name = request.POST['username'])
                    pwd = request.POST['password']
                    h1 = hashlib.md5()
                    h1.update(pwd.encode(encoding = 'utf-8'))
                    pwd = h1.hexdigest()
                    pwd_std = user_std.pwd
                    if pwd == pwd_std:
                        request.session['is_login'] = True
                        request.session['username'] = request.POST['username']
                        request.session['user_state'] = user_std.state_id if user_std.state_id else ""
                        request.session['user_voted'] = user_std.voted_id if user_std.voted_id else ""
                        message = "Login Successful!"
                        login_log_ = login_log(timestamp = time.mktime(datetime.datetime.now().timetuple()),
                                               content = "{} login".format(request.POST['username']))
                        login_log_.save(using = 'superadmin')
                    else:
                        message = "Wrong password!"
                except ObjectDoesNotExist:
                    message = "Invalid username!"
        elif "register" in request.POST:
            if request.session.get('is_login', False):
                message = "login ed!"
            elif len(request.POST['username']) < 3 or \
                    request.POST['username'].lower() == 'guest' or \
                    request.POST['username'].lower() == 'root':
                message = "Username is invalid!"
            else:
                user_ite = None
                try:
                    user_list = user.objects.get(name = request.POST['username'])
                    message = "Username exists!"
                except ObjectDoesNotExist:
                    pass
                if user_ite is None:
                    pwd = request.POST['password']
                    h1 = hashlib.md5()
                    h1.update(pwd.encode(encoding = 'utf-8'))
                    pwd = h1.hexdigest()
                    
                    state_ite = None
                    try:
                        state_ite = state_info.objects.get(state = request.POST['state'])
                    except ObjectDoesNotExist:
                        message = "State invalid!"
                    
                    if state_ite:
                        user_ = user(name = request.POST['username'], pwd = pwd, state = state_ite, authority = 1)
                        user_.save(using = 'superadmin')
                        message = "Register successful!"
                        login_log_ = login_log(timestamp = time.mktime(datetime.datetime.now().timetuple()),
                                               content = "{} registed".format(user_.name))
                        login_log_.save(using = 'superadmin')
        
        elif "logout" in request.POST:
            if not request.session.get('is_login', False):
                message = "logout ed!"
            else:
                username = request.session['username']
                request.session.flush()
                message = "Logout Successful!"
                login_log_ = login_log(timestamp = time.mktime(datetime.datetime.now().timetuple()),
                                       content = "{} logout".format(username))
                login_log_.save(using = 'superadmin')
        elif "vote_candidate" in request.POST:
            username = request.session['username']
            if request.POST['vote_candidate'] == "#biden-left":
                candidate_name = "Joe Biden"
            else:
                candidate_name = "Donald Trump"
            
            user_ite = None
            try:
                user_ite = user.objects.get(name = username)
            except ObjectDoesNotExist:
                message = "failed to find user {}".format(username)
            
            state_ite = None
            if user_ite:
                try:
                    state_ite = state_info.objects.get(state = user_ite.state_id)
                except ObjectDoesNotExist:
                    message = "failed to find state {}".format(user_ite.state_id)
                except AttributeError:
                    message = "config state first !"
            
            candidate_ite = None
            if user_ite and state_ite:
                try:
                    candidate_ite = candidate.objects.get(name = candidate_name)
                except ObjectDoesNotExist:
                    message = "failed to find candidate {}".format(candidate_name)
            
            if user_ite and state_ite and candidate_ite:
                try:
                    if user_ite.voted is None:
                        user_ite.voted = candidate_ite
                        state_vote_ite = state_vote.objects.get(state = state_ite, candidate = candidate_ite)
                        state_vote_ite.votes += 1
                        user_ite.save(using = 'superadmin')
                        state_vote_ite.save(using = 'superadmin')
                        request.session['user_voted'] = candidate_ite.name
                        message = "vote {} success !".format(candidate_ite.name)
                    else:
                        message = "failed to vote {}, already voted {}!".format(candidate_ite.name, user_ite.voted.name)
                except ObjectDoesNotExist:
                    message = "failed to find state_vote {} {}".format(user_ite.state_id, candidate_name)
        else:
            message = ""
    else:
        message = ""
    context['message'] = message
    return render(request, 'welcome.html', context)
