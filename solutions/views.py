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
from .models import submissions
# Create your views here.


def user_solution(request):

    if request.method=='POST' :
        id = request.POST.get('username')
        prob = request.POST.get('problem')
        cont = request.POST.get('contestno')
        s = cont
        s3 = prob
        s4 = id
        s2 = 'https://www.codechef.com/{}/status/{}?sort_by=All&sorting_order=asc&language=All&status=All&handle={}&Submit=GO'.format(s,s3,s4)
        url = s2

        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.content,'html.parser')
        tab = soup.find(class_='dataTable')
        # handling NoneType error
        if(tab==None):
            return render(request,'solution.html',{'success':False})

        # print(tab.prettify())
        id = tab.find_all('tr')
        print(id)
        my_list = []
        the_list = []
        for i in range(1,len(id)):

            x = id[i].find_all('td')
            a = []
            zx = {}
            start = x[1].text
            source_date = parse(start)
            source_time_zone = pytz.timezone('Europe/Moscow')
            source_date_with_timezone = source_time_zone.localize(source_date)
            target_time_zone = pytz.timezone('Asia/Kolkata')
            target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
            s= target_date_with_timezone
            k=s.replace(tzinfo=None)

            a.append(x[0].text)
            a.append(start)
            a.append(x[2].text)
            a.append(x[3].text)
            a.append(x[4].text)
            a.append(x[5].text)
            a.append(x[6].text)
            link1 = "https://www.codechef.com/viewsolution/" + x[0].text
            view_link = '<a href="{}">View</a>'.format(link1)
            a.append(view_link)
            my_list.append(a)
            zx[0] = x[0].text
            zx[1] = x[1].text
            zx[2] = x[2].text
            zx[3] = x[3].text
            zx[4] = x[4].text
            zx[5] = x[5].text
            zx[6] = x[6].text
            zx[7] = link1
            the_list.append(zx)
        my_dict = {'my_list':my_list ,'the_list':the_list,'success':True }
        return render(request,'solution.html',my_dict)

    else :
        return render(request,'solution.html')



def cf_submissions(request):
    if request.method=='POST' :
        id = request.POST.get('username')
        prob = request.POST.get('problem')
        cont = request.POST.get('contestno')
        s = ' https://codeforces.com/api/user.status?handle={}&from=1'.format(id)
        r = requests.get(s)
        r1  = r.json()
        r2 = r1['result']
        print(type(r2))
        print(cont)
        print(prob)
        l = []
        for x in r2:
            print(x['problem']['contestId'])
            print(x['problem']['index'])
            if x['problem']['contestId']==int(cont) and x['problem']['index']==prob:
                l.append(x)

        my_list = []
        for x in l:
            my_dict = {}
            my_dict[0]=x['id']
            my_dict[1]=x['problem']['name']
            my_dict[2]=x['problem']['rating']
            s = ""
            for y in x['problem']['tags']:
                s = s + y + " , "
            my_dict[3]=s
            my_dict[4]=x['verdict']
            my_dict[5]=x['programmingLanguage']
            s = "https://codeforces.com/contest/{}/submission/{}".format(cont,my_dict[0])
            my_dict[6]=s
            my_list.append(my_dict)

        dict = {'my_list':my_list}
        return render(request,'cf_submit.html',dict)

    else :
        return render(request,'cf_submit.html')
