from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from votedb.models import tweet, user_like_tweet
import datetime
import time


def str2unix(s):
    s = s.strip()
    d = datetime.datetime.strptime(s, "%Y-%m-%d")
    return int(time.mktime(d.timetuple()))


def renew_tweet_list(request):
    filter = {}
    if request.POST:
        if 'likes_limit' in request.POST:
            likes_limit = int(request.POST['likes_limit'])
            filter['likes__gte'] = likes_limit
        if 'retweet_limit' in request.POST:
            retweet_limit = int(request.POST['retweet_limit'])
            filter['retweet__gte'] = retweet_limit
        if 'username' in request.POST and 'username' != "":
            username = request.POST['username']
            filter['username__icontains'] = username
        if 'contains_text' in request.POST and 'contains_text' != "":
            contains_text = request.POST['contains_text']
            filter['text__icontains'] = contains_text
    
    return tweet.objects.filter(**filter)


def tweet_url(request):
    if "likes_tweet_id" in request.POST:
        try:
            tweet_ite = tweet.objects.get(id = request.POST["likes_tweet_id"])
            tweet_ite.likes += 1
            tweet_ite.save(using='superadmin')
            user_like_tweet_ite = user_like_tweet(name = request.session["username"], tweet_id = request.POST["likes_tweet_id"])
            user_like_tweet_ite.save(using='superadmin')
        except ObjectDoesNotExist:
            pass
    
    if "drop_id" in request.POST:
        try:
            tweet.objects.get(id = request.POST["drop_id"]).delete(using='superadmin')
        except ObjectDoesNotExist:
            pass
    
    if "new_tweet_content" in request.POST:
        username_ite = request.session["username"] \
            if "is_login" in request.session and request.session["is_login"] else "Guest"
        tweet_ite = tweet(create_time = int(time.time()),
                          text = request.POST["new_tweet_content"],
                          likes = 0,
                          retweet = 0,
                          username = username_ite,
                          user_screen_name = username_ite,
                          )
        tweet_ite.save(using='superadmin')
    
    tweet_list = renew_tweet_list(request)
    
    tweet_create_time_list = []
    user_like_tweet_list = []
    
    if 'username' in request.session:
        user_like_tweet_raw_list = user_like_tweet.objects.filter(name = request.session['username'])
    else:
        user_like_tweet_raw_list = []
    user_like_tweet_raw_set = set()
    for _ in user_like_tweet_raw_list:
        user_like_tweet_raw_set.add(_.tweet_id)
    for tweet_ite in tweet_list:
        tweet_create_time_list.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tweet_ite.create_time)))
        user_like_tweet_list.append(tweet_ite.id in user_like_tweet_raw_set)
    
    tweet_list = list(zip(tweet_list, tweet_create_time_list, user_like_tweet_list))
    tweet_list.sort(key = lambda x: -x[0].create_time)
    
    context = {
        "tweet_list":    tweet_list,
        "total":         len(tweet_list) if tweet_list else 0,
        "likes_limit":   request.POST["likes_limit"]
                         if request.POST and "likes_limit" in request.POST else 0,
        "retweet_limit": request.POST["retweet_limit"]
                         if request.POST and "retweet_limit" in request.POST else 0,
        "username":      request.POST["username"]
                         if request.POST and "username" in request.POST else "",
        "contains_text": request.POST["contains_text"]
                         if request.POST and "contains_text" in request.POST else ""
    }
    return render(request, "tweet.html", context)
