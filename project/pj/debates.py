from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from votedb.models import debate, debate_script


def debates_url(request):
    debates_list = debate.objects.all()
    
    if request.POST and 'select_debate' in request.POST:
        title = request.POST['select_debate']
    else:
        title = debates_list[0].title
    
    try:
        debate_ite = debate.objects.get(title = title)
        debate_script_list = list(debate_script.objects.filter(debate_id = debate_ite.id))
    except ObjectDoesNotExist:
        debate_script_list = []
    debate_script_list.sort(key = lambda x: x.step)
    context = {'debates_list': debates_list, 'debate_script': debate_script_list, 'debate_ite': debate_ite}
    return render(request, "debates.html", context)
