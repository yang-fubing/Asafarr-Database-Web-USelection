import numpy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

from votedb.models import state_vote, state_info, history_vote_record, state_total_vote
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt


def votes_url(request):
    update_valid = request.POST and 'update_votes_id' in request.POST
    if update_valid:
        party = request.POST['update_votes_id'][:3]
        state = request.POST['update_votes_id'][10:]
        if party == 'rep':
            name = "Donald Trump"
        else:
            name = "Joe Biden"
        try:
            state_vote_ite = state_vote.objects.get(state=state, candidate = name)
            state_vote_ite.votes = int(request.POST['update_votes_new'])
            state_vote_ite.save(using='superadmin')
        except ObjectDoesNotExist:
            pass
    
    votes_dict = {}
    
    total_votes_data = state_total_vote.objects.all()
    for _ in total_votes_data:
        votes_dict[_.state_id] = {'tot': _.votes}

    votes_data = state_vote.objects.filter(Q(candidate = "Joe Biden") | Q(candidate = "Donald Trump"))
    for _ in votes_data:
        votes_dict[_.state_id]["state"] = _.state_id
        if _.candidate_id == 'Joe Biden':
            votes_dict[_.state_id]['DEM'] = int(_.votes)
        elif _.candidate_id == 'Donald Trump':
            votes_dict[_.state_id]['REP'] = int(_.votes)

    state_info_list = state_info.objects.values('state', 'state_abbr', 'state_vote_num').all()
    for _ in state_info_list:
        if _['state'] in votes_dict:
            votes_dict[_['state']]['state_abbr'] = _['state_abbr']
            votes_dict[_['state']]['state_vote_num'] = _['state_vote_num']
            votes_dict[_['state']]['REP_percent'] = votes_dict[_['state']]['REP'] / votes_dict[_['state']]['tot'] * 100
            votes_dict[_['state']]['DEM_percent'] = votes_dict[_['state']]['DEM'] / votes_dict[_['state']]['tot'] * 100
    
    votes_list = []
    for k, v in votes_dict.items():
        votes_list.append(v)
    votes_list.sort(key=lambda x: x["state"])

    name = "Alabama"

    if request.POST:
        if "select_state" in request.POST:
            name = request.POST["select_state"]

    state_votes = None
    for _ in votes_list:
        if name == _["state"]:
            state_votes = _
    
    try:
        state_info_ite = state_info.objects.get(state = name)
    
        response_history = history_vote_record.objects.filter(state=name)
    
        plt.figure(num=1, figsize=(6, 4))
        y_DEM, y_REP = {}, {}
        for _ in response_history:
            if _.party == "DEM":
                if _.record_year not in y_DEM:
                    y_DEM[_.record_year] = 0
                y_DEM[_.record_year] += _.votes
            else:
                if _.record_year not in y_REP:
                    y_REP[_.record_year] = 0
                y_REP[_.record_year] = _.votes
        x, y = [], []
        for _ in range(1976, 2024, 4):
            if _ in y_DEM:
                x.append(_)
                y.append(y_DEM[_])
        l_DEM = plt.plot(x, y, 'b--', label='DEM')
        x, y = [], []
        for _ in range(1976, 2024, 4):
            if _ in y_REP:
                x.append(_)
                y.append(y_REP[_])
        l_REP = plt.plot(x, y, 'r--', label='REP')
        plt.title('U.S. elections in %s' % {name})
        plt.xlabel('years')
        plt.ylabel('votes')
        plt.xticks(numpy.arange(1976, 2024, 8))
        plt.legend(framealpha=0)
        save_png_name = 'US_elections_in_%s.png' % {name}
        plt.savefig("statics/media/" + save_png_name, transparent=True)
        plt.close()
        state_votes["info"] = state_info_ite
    except ObjectDoesNotExist:
        save_png_name = ""
    context = {"votes_list": votes_list, "state_votes": state_votes, "img": save_png_name}
    return render(request, "votes.html", context)
