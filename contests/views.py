from django.shortcuts import render,redirect
from .models import CF_Contest,CC_Contest
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
# Create your views here.
def CF_Schedule(request):
    CF_scrape()
    context = {'object_list':CF_Contest.objects.filter(starting__gt=datetime.datetime.now()).order_by('starting')}
    return render(request,'contests/CF_Schedule.html',context)
def CC_Schedule(request):
    CC_Scrape()
    context = {
    'present_contest_list':CC_Contest.objects.filter(start__lt = datetime.datetime.now()).order_by('start'),
    'future_contest_list':CC_Contest.objects.filter(start__gt=datetime.datetime.now()).order_by('start')
    }
    return render(request,'contests/CC_Schedule.html',context)
def CF_scrape():
    url = 'https://codeforces.com/contests'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    ContestList = soup.select_one('table').find_all('tr')
    # print(ContestList)
    for i in range(1,len(ContestList)):
        id = int(ContestList[i]['data-contestid'].strip())
        # print(id)
        contest_detail = ContestList[i].find_all('td')
        # print(contest_detail)
        name = contest_detail[0].text
        # print(name)
        writers = contest_detail[1].text
        start = contest_detail[2].text

        source_date = parse(start)
        source_time_zone = pytz.timezone('Europe/Moscow')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        s= target_date_with_timezone
        k=s.replace(tzinfo=None)

        # print(k)
        length = contest_detail[3].text
        obj, created = CF_Contest.objects.get_or_create(contestId=id)
        # print(created)
        if created:
            obj.name = name
            obj.writers = writers
            obj.starting = k
            obj.length = length
        obj.save()
def CC_Scrape():
    url = 'https://www.codechef.com/contests'
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.content,'html.parser')

    tableList = soup.find_all('table',{'class':'dataTable'})
    print(len(tableList))

    # print(tableList[0].find_all('tr')[1].find_all('td'))
    # print('present contests')

    for j in range(0,2):
        ContestList = tableList[j].find_all('tr')
        for i in range (1,len(ContestList)):
            contest_detail = ContestList[i].find_all('td')
            code = contest_detail[0].text.strip()
            name = contest_detail[1].find('a').text.strip()
            contestLink = contest_detail[1].find('a').get('href').strip()
            start = parse(contest_detail[2].get('data-starttime'))
            end = parse(contest_detail[3].get('data-endtime'))
            start = start.replace(tzinfo=None)
            end = end.replace(tzinfo=None)
            contestLink = "https://codechef.com"+contestLink
            # print(Code)
            # print(Name)
            # print(start)
            # print(end)
            obj, created = CC_Contest.objects.get_or_create(contestCode=code)
            if created:
                obj.contestCode = code
                obj.name = name
                obj.contest_link =contestLink
                obj.start = start
                obj.end = end
            obj.save()
    # print("-------------------")

def Contest(request):
    return render(request,'contests/contest.html')
