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

# Create your views here.

class Userdata :
    attempted = int()
    solved = int()




# Create your views here.

def charts(request):
    return render(request,'charts/charts.html')


def get_data(request):
    data = dict()
    if request.method == 'GET' :
        id = request.GET.get('handle')
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
                        # zx = x['problem']['rating']
                        # if zx in level:
                        #     level[zx] = level[zx] + 1
                        # else :
                        #     level[zx] = 0

                        for y in x['problem']['tags']:
                            if y in tags:
                                tags[y] = tags[y] + 1
                            else:
                                tags[y] = 0
                data['tags'] =tags
                # print(data['tags'])
                data['success'] = True

            else:
                data['success'] = False
        else:
            data['success'] = False
    else:
        data['success'] = False
    return JsonResponse(data)
