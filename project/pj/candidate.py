from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.shortcuts import render
from votedb.models import candidate


def fetch_candidate_list():
    with connection.cursor() as cursor:
        cursor.execute("create or replace view candidate_list as select name, party from votedb_candidate")


def candidate_url(request):
    sql_filter = ""
    name_query_valid = 'name' in request.POST and request.POST['name'] != ""
    party_query_valid = 'party' in request.POST and request.POST['party'] != ""
    select_query_valid = 'select_candidate' in request.POST and request.POST['select_candidate'] != ""

    def append_sql_filter(pre, suf):
        if pre == "":
            res = "where " + suf
        else:
            res = pre + " and " + suf
        return res
    
    if request.POST:
        if name_query_valid:
            sql_filter = append_sql_filter(sql_filter, "name like '%{}%'".format(request.POST['name']))
        if party_query_valid:
            sql_filter = append_sql_filter(sql_filter, "party = '{}'".format(request.POST['party']))
    
    sql_string = "select * from candidate_list {}".format(sql_filter)
    
    with connection.cursor() as cursor:
        cursor.execute(sql_string)
        candidate_list = cursor.fetchall()

    candidate_list = list(candidate_list)
    
    candidate_list_cursor = 0
    
    for idx in range(len(candidate_list)):
        if candidate_list[idx][0] == "Joe Biden":
            t = candidate_list[candidate_list_cursor]
            candidate_list[candidate_list_cursor] = candidate_list[idx]
            candidate_list[idx] = t
            candidate_list_cursor += 1
            break

    for idx in range(len(candidate_list)):
        if candidate_list[idx][0] == "Donald Trump":
            t = candidate_list[candidate_list_cursor]
            candidate_list[candidate_list_cursor] = candidate_list[idx]
            candidate_list[idx] = t
            break

    if select_query_valid:
        name = request.POST['select_candidate']
    elif len(candidate_list) > 0:
        name = candidate_list[0][0]
    else:
        name = None
    
    if name:
        try:
            candidate_ite = candidate.objects.get(name = name)
            description = candidate_ite.description
            pic = candidate_ite.pic
        except ObjectDoesNotExist:
            description = "unknown"
            pic = "unknown.png"
    else:
        description = "unknown"
        pic = "unknown.png"

    context = {
        'candidate_list': candidate_list,
        'query_name':     request.POST['name'] if name_query_valid else "",
        'query_party':    request.POST['party'] if party_query_valid else "",
        'description':    description,
        'pic':            pic
    }
    
    return render(request, "candidate.html", context)
