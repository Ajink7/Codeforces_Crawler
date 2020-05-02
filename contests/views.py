from django.shortcuts import render,redirect
from .models import Contest
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
# Create your views here.
def contest(request):
    scrape(request)
    context = {'object_list':Contest.objects.filter(starting__gt=datetime.datetime.now()).order_by('starting')}
    return render(request,'contests/contest.html',context)

def scrape(request):
    url = 'https://codeforces.com/contests'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    ContestList = soup.select_one('table').find_all('tr')
    # print(ContestList)
    for i in range(1,len(ContestList)):
        id = int(ContestList[i]['data-contestid'].strip())
        print(id)
        contest_detail = ContestList[i].find_all('td')
        # print(contest_detail)
        name = contest_detail[0].text
        print(name)
        writers = contest_detail[1].text
        start = contest_detail[2].text

        source_date = parse(start)
        source_time_zone = pytz.timezone('Europe/Moscow')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        s= target_date_with_timezone
        k=s.replace(tzinfo=None)

        print(k)
        length = contest_detail[3].text
        obj, created = Contest.objects.get_or_create(contestId=id)
        print(created)
        if created:
            obj.name = name
            obj.writers = writers
            obj.starting = k
            obj.length = length
        obj.save()
