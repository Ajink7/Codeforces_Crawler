from django.shortcuts import render
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.core.serializers import serialize
import json
# Create your views here.

class Userdata:
    username = str()
    total_submission = int()
    accepted = int()
    tags = list()
    prob_rating = list()
    verdicts = list()
    def __init__(self):
        return
    def __str__(self):
        return self.username

class Tag:
    name = str()
    count = int()
    def __str__(self):
        return self.name

class ProbRating:
    rating = int()
    count = int()
    def __str__():
        return self.rating

class Verdict:
    verdict = ""
    count = int()
    def __str__(self):
        return self.verdict



def charts(request):
    return render(request,'charts/charts.html')


def get_data(request):
    data = dict()
    if request.method == 'GET' and request.is_ajax():
        handle = request.GET.get('handle')
        url = ' https://codeforces.com/api/user.status?handle={}&from=1'.format(handle)
        r = requests.get(url)
        if r.status_code==200:
            json_data  = r.json()
            if json_data['status']=='OK':
                result = json_data['result']
                user = Userdata()
                user.total_submission = len(result)
                user.accepted = 0
                level = {}
                tags = {}
                verdicts = {}
                for x in result:
                    if x['verdict'] in verdicts:
                        verdicts[x['verdict']] = verdicts[x['verdict']] + 1
                    else:
                        verdicts[x['verdict']] = 0
                    if x['verdict']=="OK" :
                        user.accepted +=1
                        for y in x['problem']['tags']:
                            if y in tags:
                                tags[y] = tags[y] + 1
                            else:
                                tags[y] = 0
                tags_list = []
                prob_rating_list = []
                verdicts_list = []
                for key , value in tags.items():
                    o1 = Tag()
                    o1.name = key
                    o1.count = value
                    tags_list.append(o1.__dict__)

                for key , value in level.items():
                    o1 = ProbRating()
                    o1.rating = key
                    o1.count = value
                    prob_rating_list.append(o1.__dict__)

                for key , value in verdicts.items():
                    o1 = Verdict()
                    o1.verdict = key
                    o1.count = value
                    verdicts_list.append(o1.__dict__)
                user.username = handle
                user.tags = tags_list
                user.prob_rating = prob_rating_list
                user.verdicts = verdicts_list
                # str_data = serialize('json', user)
                # user = json.loads(str_data)
                data['user_data'] = user.__dict__
                # print(user.tags)
                data['success'] = True

            else:
                data['success'] = False
        else :
            data['success'] = False
    else:
        data['success'] = False
    # print(data)
    return JsonResponse( data)
