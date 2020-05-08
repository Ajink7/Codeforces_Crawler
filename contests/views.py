from django.shortcuts import render,redirect
from .models import CF_Contest,CC_Contest,Contests
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession
from operator import itemgetter
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

def Contest(request):
    contests = Contests.objects.all().order_by('starting')
    return render(request,'contests/contest.html',{'contests':contests})
# format for each list of contest:
# [Contest ID/code,starting time,duration,Contest Name, Contest Link]
# will sort by starting time

def ajax_update_contests(request):
    data = dict()
    if request.is_ajax() and request.method=='GET':
        # print("got an ajax request...")
        # print("cleaning database...")
        Contests.objects.all().delete()
        # print("database cleaned!")
        # print("scraping cf... ")
        CF_scrape();
        # print("scraping cc...")
        CC_Scrape();
        # print("scraping done!")
        contests = Contests.objects.all().order_by('starting')
        data['html_contests_data'] = render_to_string('contests/partial_contests.html',{'contests':contests})
        data['success']=True
    # print("returning json response....")
    return JsonResponse(data)


def cf_list():
    data_list =[]
    url = 'https://codeforces.com/contests'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    ContestList = soup.select_one('table').find_all('tr')
    for i in range(1,len(ContestList)):
        id = ContestList[i]['data-contestid'].strip()
        # print(id)
        contest_detail = ContestList[i].find_all('td')
        # print(contest_detail)
        name = contest_detail[0].text
        # print(name)
        writers = contest_detail[1].text
        start = contest_detail[2].text
        # print(start)
        source_date = parse(start)
        source_time_zone = pytz.timezone('Europe/Moscow')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        s= target_date_with_timezone
        k=s.replace(tzinfo=None)

        # print(k)
        length = contest_detail[3].text
        d = []
        d.append(id)
        d.append(k)
        d.append(length)
        d.append(name)
        link = "https://codeforces.com/contestRegistration/"+id
        link = "<a href=\"{link}\" class=\"btn btn-success\">Register</a>".format(link=link)
        d.append(link)
        data_list.append(d)
    return data_list

def cc_list():
    url = 'https://www.codechef.com/contests'
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.content,'html.parser')

    tableList = soup.find_all('table',{'class':'dataTable'})
    # print(len(tableList))

    # print(tableList[0].find_all('tr')[1].find_all('td'))
    # print('present contests')

    for j in range(0,2):
        data_list =[]
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
            contestLink = "<a href=\"{link}\" class=\"btn btn-success\">Register</a>".format(link=contestLink)

            # # print(Code)
            # print(name)
            # print(start)
            # print(end)
            # print(end-start)
            # print("...................")
            d = []
            d.append(code)
            d.append(start)
            d.append(end-start)
            d.append(name)
            d.append(contestLink)
            data_list.append(d)
    print(data_list)
    return data_list



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
        id = ContestList[i]['data-contestid'].strip()
        # print(id)
        contest_detail = ContestList[i].find_all('td')
        # print(contest_detail)
        name = contest_detail[0].text
        # print(name)
        writers = contest_detail[1].text
        start = contest_detail[2].text
        # print(start)
        source_date = parse(start)
        source_time_zone = pytz.timezone('Europe/Moscow')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        s= target_date_with_timezone
        k=s.replace(tzinfo=None)
        link = "https://codeforces.com/contestRegistration/"+id

        # print(k)
        length = contest_detail[3].text
        obj, created = Contests.objects.get_or_create(code=id)
        # print(created)
        if created:
            obj.name = name
            obj.link = link
            obj.starting = k
            obj.duration = length
        obj.save()
def CC_Scrape():
    url = 'https://www.codechef.com/contests'
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.content,'html.parser')

    tableList = soup.find_all('table',{'class':'dataTable'})
    # print(len(tableList))

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
            obj, created = Contests.objects.get_or_create(code=code)
            if created:
                obj.code = code
                obj.name = name
                obj.link =contestLink
                obj.starting = start
                obj.duration = end-start
            obj.save()
    # print("-------------------")

def leetcode_scrape():
    pass
    # url = "https://leetcode.com/contest/"
    # rec  = requests.get(url)
    # try:
    #     rec.raise_for_status()
    # except requests.exceptions.HTTPError as e:
    #     print(e)
    # soup = bs4.BeautifulSoup(rec.content,'html.parser')
    # contest_card = soup.find_all(class_="contest-card-base")
    # print(contest_card)
    # print(contest_card[0].prettify())
    # opts = Options()
    # opts.headless = True
    # driver = Firefox(options=opts)
    # try:
    #     driver.get('url')
    # finally:
    #     driver.quit()
    #
    # return
def cf_scrape2(request):
    session = HTMLSession()
    r = session.get('https://codeforces.com/contests')

    table = r.html.find('table')[0]

    table_rows =table.find('tr')

    table_headers = table_rows[0].find('th')

    headers=[]
    headers.append('Contest ID')

    for th in table_headers:
        headers.append(th.text)
    headers.pop(len(headers)-1)
    headers.pop(len(headers)-1)
    headers.append("Registration Link")
    table_rows.pop(0)

    table_data =[]
    for tr in table_rows:
        d = []
        # print(tr.attrs)
        id = tr.attrs.get('data-contestid')
        d.append(id)
        table_td = tr.find('td')
        for td in table_td:
            d.append(td.text)
        d.pop(len(d)-1)
        d.pop(len(d)-1)
        link = "https://codeforces.com/contestRegistration/"+id
        a_tag = "<a href=\"{link}\" class=\"btn btn-success\">Register</a>".format(link=link)
        d.append(a_tag)
        table_data.append(d)
    # print(headers)
    # print(table_data)
    r.close()
    context = {'headers':headers,'table_data':table_data}
    return render(request,'contests/cf_schedule2.html',context)


def atcoder_scrape(request):
    session = HTMLSession()
    r = session.get('https://atcoder.jp/contests/')
    tabel_html = r.html.find('#contest-table-upcoming')[0].html
    print(tabel_html)
    return render(request,'contests/atcoder_schedule.html',{'table_html':tabel_html})
