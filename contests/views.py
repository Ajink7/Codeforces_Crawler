from django.shortcuts import render,redirect
from .models import *
from .scrape_helper import *
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q


def Contest(request):
    contests = Contests.objects.all().filter(Q(starting__gt=datetime.datetime.now())|Q(ending__gt=datetime.datetime.now(),platform='codechef')).order_by('starting')
    return render(request,'contests/contest.html',{'contests':contests})


#  funtion to filter table-data
def ajax_filter(request):
    data = dict()
    if request.is_ajax() and request.method=='GET':
        cc = request.GET.get('cc')
        cf  =request.GET.get('cf')
        ac = request.GET.get('ac')
        lc = request.GET.get('lc')
        contests = Contests.objects.all().filter(Q(starting__gt=datetime.datetime.now())|Q(ending__gt=datetime.datetime.now(),platform='codechef')).order_by('starting')
        # TODO: get valid contests only
        if(cc=="false"):
            contests = contests.exclude(platform="codechef")
        if(cf=="false"):
            contests = contests.exclude(platform="codeforces")
        if(ac=="false"):
            contests = contests.exclude(platform="atcoder")
        if(lc=="false"):
            contests = contests.exclude(platform="leetcode")
        data['success']=True
        data['html_contests_data'] = render_to_string('contests/partial_contests.html',{'contests':contests})
    return JsonResponse(data)



# function to update our database

def ajax_update_contests(request):
    data = dict()
    if request.is_ajax() and request.method=='GET':
        # print("got an ajax request...")
        # print("scraping cf... ")
        id_list =CF_scrape();
        # print("scraping cc...")
        CC_Scrape();
        if not id_list:
            pass
        else:
            print(' '.join(id_list))
            Contests.objects.filter(Q(platform='codeforces')).exclude(code__in=id_list).delete()
        # scraping atcoder
        atcoder_scrape();
        # updating leetcode contest
        leetcode_update()
        # # print("scraping done!")
        data['success']=True
    # print("returning json response....")
    return JsonResponse(data)
