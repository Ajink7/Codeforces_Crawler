
from django.shortcuts import render
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

class Userdata :
    attempted = int()
    solved = int()
    tag = list()
    rating = list()
    o = list()
    def __init__(self):
        return
class prob:
    name = str()
    count = int()
    def __init__(self):
        return

class prob_rating:
    rating = int()
    count = int()
    def __init__(self):
        return
class v:
    output = ""
    count = int()
    def __init__(self):
        return

# Create your views here.
def get_profile(request):
    data = {}
    if request.method == 'POST' :

        id = request.POST.get('handle')
        s = ' https://codeforces.com/api/user.status?handle={}&from=1'.format(id)
        r = requests.get(s)
        if r.status_code==200:
            json_data  = r.json()
            if json_data['status']=='OK':
                r2 = json_data['result']
                user1 = Userdata()
                user1.attempted = len(r2)
                user1.solved = 0
                level = {}
                tags = {}
                verdicts = {}
                for x in r2:
                    if x['verdict'] in verdicts:
                        verdicts[x['verdict']] = verdicts[x['verdict']] + 1
                    else:
                        verdicts[x['verdict']] = 0
                    if x['verdict']=="OK" :
                        user1.solved = user1.solved + 1
                        zx = x['problem']['rating']
                        if zx in level:
                            level[zx] = level[zx] + 1
                        else :
                            level[zx] = 0

                        for y in x['problem']['tags']:
                            if y in tags:
                                tags[y] = tags[y] + 1
                            else:
                                tags[y] = 0

                l1 = []
                l2 = []
                l3 = []
                for key , value in tags.items():
                    o1 = prob()
                    o1.name = key
                    o1.count = value
                    l1.append(o1)

                for key , value in level.items():
                    o1 = prob_rating()
                    o1.rating = key
                    o1.count = value
                    l2.append(o1)

                for key , value in verdicts.items():
                    o1 = v()
                    o1.output = key
                    o1.count = value
                    l3.append(o1)

                user1.tag = l1
                user1.rating = l2
                user1.o = l3

                data['user1'] = user1
                data['success'] = True

            else:
                data['success'] = False
        else :
            data['success'] = False

        return render(request,'cf_profile.html',data)
    else:
        data['success'] = False
        return render(request,'cf_profile.html',data)
