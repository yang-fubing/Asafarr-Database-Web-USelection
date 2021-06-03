import hashlib
from datetime import datetime

import django
from django.http import HttpResponse

from votedb.models import *

django.setup()


description_dict = {
    "Donald Trump": [
        """
    <h1><b>Donald John Trump</b></h1>
<p>
    Donald Trump (born June 14, 1946) is an American media personality and businessman who served as the 45th president of the United States from 2017 to 2021.
    Trump's political positions have been described as populist, protectionist, isolationist, and nationalist. He entered the 2016 presidential race as a Republican and was elected in an upset victory over Democratic nominee Hillary Clinton while losing the popular vote.[a] He was the first U.S. president without prior military or government service. His election and policies sparked numerous protests. Trump made many false and misleading statements during his campaigns and presidency, to a degree unprecedented in American politics. Many of his comments and actions have been characterized as racially charged or racist.
</p>
<p>
    During his presidency, Trump ordered a travel ban on citizens from several Muslim-majority countries, citing security concerns; after legal challenges, the Supreme Court upheld the policy's third revision. He enacted the Tax Cuts and Jobs Act of 2017 which cut taxes for individuals and businesses and rescinded the individual health insurance mandate penalty of the Affordable Care Act. He appointed Neil Gorsuch, Brett Kavanaugh and Amy Coney Barrett to the Supreme Court as well as more than 200 federal judges. In foreign policy, Trump pursued an America First agenda: he renegotiated the North American Free Trade Agreement as the U.S.–Mexico–Canada Agreement and withdrew the U.S. from the Trans-Pacific Partnership trade negotiations, the Paris Agreement on climate change and the Iran nuclear deal. He imposed import tariffs that triggered a trade war with China and met three times with North Korean leader Kim Jong-un, but negotiations on denuclearization eventually broke down. Trump reacted slowly to the COVID-19 pandemic, ignored or contradicted many recommendations from health officials in his messaging, and promoted misinformation about unproven treatments and the availability of testing.
</p>
<p>
    A special counsel investigation led by Robert Mueller found that Russia interfered in the 2016 election with the goal of helping Trump's election chances, but did not find sufficient evidence to establish criminal conspiracy or coordination with Russia.[b] Mueller also investigated Trump for obstruction of justice and neither indicted nor exonerated him. The House of Representatives impeached Trump on December 18, 2019 for abuse of power and obstruction of Congress after he solicited Ukraine to investigate Joe Biden. The Senate acquitted him of both charges on February 5, 2020.</p>
<p>
    Trump lost the 2020 presidential election to Biden, but refused to concede defeat. He attempted to overturn the results by making false claims of electoral fraud, pressuring government officials, mounting scores of unsuccessful legal challenges and obstructing the presidential transition. On January 6, 2021, Trump urged his supporters to march to the Capitol, which hundreds stormed, interrupting the electoral vote count. On January 13, the House impeached Trump for incitement of insurrection, making him the only federal officeholder in American history to be impeached twice. The Senate acquitted Trump for the second time on February 13.
</p>
        """
        , "trump.jpg"],
    "Joe Biden":    [
        """
<h1><b>Joseph Robinette Biden Jr.</b></h1>
<p>
Joe Biden,is an American politician who is the 46th and current president of the United States. A member of the Democratic Party, he served as the 47th vice president from 2009 to 2017 under Barack Obama and represented Delaware in the United States Senate from 1973 to 2009.
</p>

<p>
Born and raised in Scranton, Pennsylvania, and later in New Castle County, Delaware, Biden studied at the University of Delaware before earning his law degree from Syracuse University in 1968. He was elected to the New Castle County Council in 1970 and became the sixth-youngest senator in the U.S. when he was elected to the United States Senate from Delaware in 1972, at age 29. Biden was a longtime member of the Senate Foreign Relations Committee and eventually became its chairman. He also chaired the Senate Judiciary Committee from 1987 to 1995, dealing with drug policy, crime prevention, and civil liberties issues; led the effort to pass the Violent Crime Control and Law Enforcement Act and the Violence Against Women Act; and oversaw six U.S. Supreme Court confirmation hearings, including the contentious hearings for Robert Bork and Clarence Thomas. He ran unsuccessfully for the Democratic presidential nomination in 1988 and 2008. Biden was reelected to the Senate six times, and was the fourth-most senior senator when he became Obama's vice president after they won the 2008 presidential election, defeating John McCain and his running mate Sarah Palin.</p>
<p>
During eight years as vice president, Biden leaned on his Senate experience and frequently represented the administration in negotiations with congressional Republicans, including on the Budget Control Act of 2011, which resolved a debt ceiling crisis, and the American Taxpayer Relief Act of 2012, which addressed the impending "fiscal cliff". He also oversaw infrastructure spending in 2009 to counteract the Great Recession. On foreign policy, Biden was a close counselor to the president and took a leading role in designing the withdrawal of U.S. troops from Iraq in 2011. In 2012, they won re-election defeating Mitt Romney and Paul Ryan. In 2017, Obama awarded Biden the Presidential Medal of Freedom with distinction, making him the first president to receive it before taking office.</p>

<p>Biden and his running mate Kamala Harris defeated incumbent president Donald Trump and vice president Mike Pence in the 2020 presidential election. Biden is the oldest elected president, the first to have a female and African-Asian American vice president, the first from Delaware, and the second Catholic President, the first bring President John F. Kennedy. His early presidential activity centered around proposing, lobbying for, and signing into law the American Rescue Plan Act of 2021 to speed up the United States' recovery from the COVID-19 pandemic and the ongoing recession, as well as a series of executive orders. Biden's orders addressed the pandemic and reversed several Trump administration policies, including by rejoining the Paris Agreement on climate change and reaffirming protections for Deferred Action for Childhood Arrivals recipients. In April 2021, Biden announced the withdrawal of all U.S. troops from Afghanistan by September 2021.</p>

        """
        , "biden.jpg"]
}


def candidate_init():
    d = {}
    with open("data/us-election-2020/candidate.csv", "r") as f:
        for _ in f.readlines():
            _ = _.strip().split(',')
            if _[1] not in d and _[1] != " Write-ins":
                d[_[1]] = _[2]
    candidate_task = []
    for k, v in d.items():
        if k in description_dict:
            description = description_dict[k][0]
            pic = description_dict[k][1]
        else:
            description = "unknown"
            pic = "unknown.png"
        candidate_ite = candidate(name = k, party = v, description = description, pic = pic)
        candidate_task.append(candidate_ite)
    candidate.objects.using('superadmin').bulk_create(candidate_task)


def state_info_init():
    state_info_task = []
    with open("data/2020-us-general-election-turnout-rates/2020 November General Election - Turnout Rates.csv",
              "r") as f:
        title = f.readline()
        for _ in f.readlines():
            _ = _.strip().split(',')
            state_info_ite = state_info(state = _[0],
                                        state_abbr = _[14],
                                        state_vote_num = int(_[15]),
                                        has_votes_right_population = int(_[6]),
                                        in_votes_ages_population = int(_[7]),
                                        prisoner_population = int(_[9])
                                        )
            state_info_task.append(state_info_ite)
    state_info.objects.using('superadmin').bulk_create(state_info_task)


def debate_init(candidate_dict):
    debate_task = [debate(title = "us_election_2020_1st_presidential_debate",
                          duration = 5707,
                          pros = candidate_dict["Donald Trump"],
                          defense = candidate_dict["Joe Biden"],
                          voice_location = "debates/us_election_2020_1st_presidential_debate.mp3",
                          ),
                   debate(title = "us_election_2020_2nd_presidential_debate",
                          duration = 5655,
                          pros = candidate_dict["Donald Trump"],
                          defense = candidate_dict["Joe Biden"],
                          voice_location = "debates/us_election_2020_2nd_presidential_debate.mp3",
                          ),
                   debate(title = "us_election_2020_biden_town_hall",
                          duration = 5502,
                          pros = candidate_dict["Donald Trump"],
                          defense = candidate_dict["Joe Biden"],
                          voice_location = "debates/us_election_2020_biden_town_hall.mp3",
                          ),
                   debate(title = "us_election_2020_trump_town_hall",
                          duration = 3610,
                          pros = candidate_dict["Donald Trump"],
                          defense = candidate_dict["Joe Biden"],
                          voice_location = "debates/us_election_2020_trump_town_hall.mp3",
                          ),
                   debate(title = "us_election_2020_vice_presidential_debate",
                          duration = 5377,
                          pros = candidate_dict["Donald Trump"],
                          defense = candidate_dict["Joe Biden"],
                          voice_location = "debates/us_election_2020_vice_presidential_debate.mp3",
                          )]
    debate.objects.using('superadmin').bulk_create(debate_task)


def state_vote_init(candidate_dict, state_info_dict):
    state_total_vote_dict = {}
    state_vote_task = []
    with open("data/us-election-2020/candidate.csv", "r") as f:
        for _ in f.readlines():
            _ = _.strip().split(',')
            
            if _[0] not in state_total_vote_dict:
                state_total_vote_dict[_[0]] = 0
            state_total_vote_dict[_[0]] += int(_[3])
            
            try:
                state_vote_ite = state_vote(state = state_info_dict[_[0]],
                                            candidate = candidate_dict[_[1]],
                                            votes = int(_[3]))
                state_vote_task.append(state_vote_ite)
            except KeyError:
                pass
    state_vote.objects.using('superadmin').bulk_create(state_vote_task)
    
    state_total_vote_task = []
    for k, v in state_total_vote_dict.items():
        state_total_vote_ite = state_total_vote(state = state_info_dict[k], votes = v)
        state_total_vote_task.append(state_total_vote_ite)
    state_total_vote.objects.using('superadmin').bulk_create(state_total_vote_task)


def tweet_init():
    tweet_task = []
    import pandas
    trump_df = pandas.read_csv('data/us-election-2020-tweets/hashtag_donaldtrump.csv',
                               lineterminator = '\n',
                               nrows = 200
                               )
    biden_df = pandas.read_csv('data/us-election-2020-tweets/hashtag_joebiden.csv',
                               lineterminator = '\n',
                               nrows = 200
                               )

    def remove_emoji(s):
        if type(s) != str:
            return ""
        s_utf8 = s.encode("ascii", "ignore")
        s_utf8 = s_utf8.decode("utf-8", "ignore")
        return s_utf8
    
    def work(csv, idx):
        date, time_ = csv['created_at'][idx].split(' ')
        year, month, day = date.split('-')
        hour, second, minute = time_.split(':')
        datetime_ = datetime(int(year), int(month), int(day),
                             int(hour), int(second), int(minute))
        import time
        datetime_unix = int(time.mktime(datetime_.timetuple()))
        tweet_ite = tweet(create_time = datetime_unix,
                          text = remove_emoji(csv['tweet'][idx]),
                          likes = int(csv['likes'][idx]),
                          retweet = int(csv['retweet_count'][idx]),
                          username = remove_emoji(csv['user_name'][idx]),
                          user_screen_name = remove_emoji(csv['user_screen_name'][idx])
                          )
        return tweet_ite
    
    for i in range(0, 100):
        tweet_task.append(work(trump_df, i))
    for i in range(0, 100):
        tweet_task.append(work(biden_df, i))
    tweet.objects.using('superadmin').bulk_create(tweet_task)


def script_process(debate_id, path):
    import pandas
    script_df = pandas.read_csv(path, lineterminator = '\n')
    single_script_task = []
    for i in range(script_df.shape[0]):
        if type(script_df['minute'][i]) == str:
            timestamp = script_df['minute'][i].split(':')
            timestamp = int(timestamp[0]) * 60 + int(timestamp[1])
        else:
            timestamp = 2e7
        debate_script_ite = debate_script(debate_id = debate_id,
                                          step = i,
                                          speaker = script_df['speaker'][i],
                                          text = script_df['text'][i],
                                          time_stamp = timestamp)
        single_script_task.append(debate_script_ite)
    return single_script_task


def debate_script_init(debate_dict):
    debate_id_start = None
    for _ in debate_dict.values():
        if debate_id_start is None:
            debate_id_start = _.id
        else:
            debate_id_start = min(debate_id_start, _.id)
    debate_script_task = []
    debate_script_task.extend(
        script_process(debate_dict[debate_id_start],
                       "data/us-election-2020-presidential-debates/us_election_2020_1st_presidential_debate.csv")
    )
    debate_script_task.extend(
        script_process(debate_dict[debate_id_start + 1],
                       "data/us-election-2020-presidential-debates/us_election_2020_2nd_presidential_debate.csv")
    )
    debate_script_task.extend(
        script_process(debate_dict[debate_id_start + 2],
                       "data/us-election-2020-presidential-debates/us_election_2020_biden_town_hall.csv")
    )
    debate_script_task.extend(
        script_process(debate_dict[debate_id_start + 3],
                       "data/us-election-2020-presidential-debates/us_election_2020_trump_town_hall.csv")
    )
    debate_script_task.extend(
        script_process(debate_dict[debate_id_start + 4],
                       "data/us-election-2020-presidential-debates/us_election_2020_vice_presidential_debate.csv")
    )
    debate_script.objects.using('superadmin').bulk_create(debate_script_task)


def user_init(state_info_dict):
    pwd = "root"
    h1 = hashlib.md5()
    h1.update(pwd.encode(encoding = 'utf-8'))
    pwd = h1.hexdigest()
    _ = user(name = "root", pwd = pwd, authority = 2)
    _.save(using='superadmin')


def login_log_init():
    _ = login_log(timestamp = 0, content = "init")
    _.save(using='superadmin')


def history_vote_record_init(state_info_dict):
    import pandas
    print("history_vote_record_init ...")
    history_vote_record_df = pandas.read_csv("data/us-elections-dataset/1976-2020-president.csv", lineterminator = '\n')
    
    history_vote_record_task = []
    
    history_vote_record_dict = {}
    for idx in range(history_vote_record_df.shape[0]):
        record_year = int(history_vote_record_df['year'][idx])
        state = history_vote_record_df['state'][idx]
        state = state[0] + state[1:].lower()
        party = (history_vote_record_df['party_detailed'][idx])
        if type(party) != str:
            continue
        party = party[:3]
        votes = history_vote_record_df['candidatevotes'][idx]
        if party != "DEM" and party != "REP":
            continue
        try:
            k = (record_year, state_info_dict[state], party)
            if k not in history_vote_record_dict:
                history_vote_record_dict[k] = 0
            history_vote_record_dict[k] += votes
        except KeyError:
            pass
    
    for k, v in history_vote_record_dict.items():
        history_vote_record_ = history_vote_record(record_year = k[0],
                                                   state = k[1],
                                                   party = k[2],
                                                   votes = v)
        history_vote_record_task.append(history_vote_record_)

    print("history_vote_record bulk_creaing ...")
    history_vote_record.objects.using('superadmin').bulk_create(history_vote_record_task)
    print("history_vote_record finish.")


def init(request):
    user_sum = len(user.objects.all())
    if user_sum == 0 or (request.session.get('is_login', True) and request.session.get('username', "") == "root"):
        debate_script.objects.using('superadmin').all().delete()
        history_vote_record.objects.using('superadmin').all().delete()
        login_log.objects.using('superadmin').all().delete()
        state_vote.objects.using('superadmin').all().delete()
        state_total_vote.objects.using('superadmin').all().delete()
        tweet.objects.using('superadmin').all().delete()
        candidate.objects.using('superadmin').all().delete()
        debate.objects.using('superadmin').all().delete()
        state_info.objects.using('superadmin').all().delete()
        user.objects.using('superadmin').all().delete()

        candidate_init()
        state_info_init()
        
        candidate_list = candidate.objects.all()
        candidate_dict = {}
        for _ in candidate_list:
            candidate_dict[_.name] = _
    
        state_info_list = state_info.objects.all()
        state_info_dict = {}
        for _ in state_info_list:
            state_info_dict[_.state] = _
    
        debate_init(candidate_dict)
        
        debate_list = debate.objects.all()
        debate_dict = {}
        for _ in debate_list:
            debate_dict[_.id] = _
    
        state_vote_init(candidate_dict, state_info_dict)
        tweet_init()
        debate_script_init(debate_dict)
        user_init(state_info_dict)
        login_log_init()
        history_vote_record_init(state_info_dict)
    
        return HttpResponse("重置结束")
    else:
        return HttpResponse("重置需要管理员权限")


if __name__ == "__main__":
    pass
