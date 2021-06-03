from django.db import models


class candidate(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    party = models.CharField(max_length = 20)
    description = models.TextField()
    pic = models.TextField()


class state_info(models.Model):
    state = models.CharField(max_length = 50, primary_key = True)
    state_abbr = models.CharField(max_length = 20)
    state_vote_num = models.IntegerField()
    has_votes_right_population = models.IntegerField()
    in_votes_ages_population = models.IntegerField()
    prisoner_population = models.IntegerField()


class state_vote(models.Model):
    state = models.ForeignKey('state_info', on_delete = models.SET_NULL, null = True)
    candidate = models.ForeignKey('candidate', on_delete = models.SET_NULL, null = True)
    votes = models.IntegerField()


class state_total_vote(models.Model):
    state = models.OneToOneField('state_info', primary_key = True, on_delete = models.CASCADE)
    votes = models.IntegerField()


class history_vote_record(models.Model):
    record_year = models.IntegerField()
    state = models.ForeignKey('state_info', on_delete = models.SET_NULL, null = True)
    party = models.CharField(max_length = 20)
    votes = models.IntegerField()
    
    class Meta:
        db_tablespace = "tables"


class tweet(models.Model):
    create_time = models.IntegerField()
    text = models.TextField()
    likes = models.IntegerField()
    retweet = models.IntegerField()
    username = models.CharField(max_length = 50)
    user_screen_name = models.CharField(max_length = 50)


class debate(models.Model):
    title = models.TextField()
    pros = models.ForeignKey('candidate', on_delete = models.SET_NULL, null = True, related_name='pros')
    defense = models.ForeignKey('candidate', on_delete = models.SET_NULL, null = True, related_name='offense')
    duration = models.IntegerField()  # second
    voice_location = models.TextField()


class debate_script(models.Model):
    debate_id = models.ForeignKey('debate', on_delete = models.SET_NULL, null = True)
    step = models.IntegerField()
    speaker = models.CharField(max_length = 50)
    text = models.TextField()
    time_stamp = models.IntegerField()


class user(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    pwd = models.CharField(max_length = 40)
    state = models.ForeignKey('state_info', on_delete = models.SET_NULL, null = True)
    authority = models.IntegerField()
    voted = models.ForeignKey('candidate', on_delete = models.SET_NULL, blank = True, null = True)


class user_like_tweet(models.Model):
    name = models.CharField(max_length = 50)
    tweet_id = models.IntegerField()


class login_log(models.Model):
    timestamp = models.IntegerField()
    content = models.TextField()
