from .models import *
import webbrowser,bs4,sys,requests
import datetime
from django.utils import timezone
import pytz
from dateutil.parser import parse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession


# format for each list of contest:
# [Contest ID/code,starting time,duration,Contest Name, Contest Link,platform,ending]


# function to scrape codeforces contests
def CF_scrape():
    id_list =[]
    url = 'https://codeforces.com/contests?complete=true'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'html.parser')
    ContestList = soup.select_one('table').find_all('tr')
    # print(ContestList)
    for i in range(1,len(ContestList)):
        id = ContestList[i]['data-contestid'].strip()
        id_list.append(id)
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
            obj.platform = "codeforces"
        obj.save()
    return id_list

# function to scrape codechef contests
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
                obj.platform = "codechef"
                obj.ending = end
            obj.save()
    # print("-------------------")

# function to scrape atcoder contests
def atcoder_scrape():
    session = HTMLSession()

    # get the html of the contests page
    r = session.get('https://atcoder.jp/contests/')

    # current contests
    tc = r.html.find('#contest-table-action')
    if(len(tc)!=0):
        tc = tc[0]
        tc_table = tc.find('tbody')[0]
        current_contests = tc_table.find('tr')
    else:
        current_contests = []
        # if there is no current contest then atcoder don't have this table

    # Future contests
    tf = r.html.find('#contest-table-upcoming')
    if(len(tf)!=0):
        tf = tf[0]
        tf_table = tf.find('tbody')[0]
        future_contest = tf_table.find('tr')
    else:
        future_contest=[]

    #  sum
    contests = current_contests+future_contest

    for contest in contests:
        td = contest.find('td')
        starting = td[0].text
        starting = starting[:len(starting)-5]
        name = td[1].find('a')[0].text
        code = td[1].find('a')[0].attrs['href']
        link = "https://atcoder.jp"+code
        code = code[10:]
        duration = td[2].text
        rated_range = td[3].text

        #  Atcoder localize the time itself
        source_date = parse(starting)
        source_time_zone = pytz.timezone('Asia/Tokyo')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        s= target_date_with_timezone
        k=s.replace(tzinfo=None)

        #
        # print(code)
        # print(link)
        # print(starting)
        # print(name)
        # print(duration)
        # print(rated_range)
        # print("-------------")

         # creating/updating new contest
        obj, created = Contests.objects.get_or_create(code=code)
        if created:
            obj.code = code
            obj.name = name
            obj.link = link
            obj.starting = k
            obj.duration = duration
            obj.platform = "atcoder"
        obj.save()


# function to update leetcode contests
def leetcode_update():
    #updating biweekly
    a = Contests.objects.get(platform='leetcode',code__startswith='BWC')
    a.starting = a.starting.replace(tzinfo=None)
    if a.starting < datetime.datetime.now():

        source_time_zone = pytz.timezone('UTC')
        source_date_with_timezone = source_time_zone.localize(a.starting)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        a.starting = target_date_with_timezone+ datetime.timedelta(days=14)
        a.starting = a.starting.replace(tzinfo=None)
        no = int(a.code[3:])
        no=no+1;
        a.code = "BWC"+str(no)
        a.name = "Biweekly Contest "+str(no)
        a.link = "https://leetcode.com/contest/biweekly-contest-"+str(no)
        # a.code = BWC+
        a.save()

    #updating weekly
    a = Contests.objects.get(platform='leetcode',code__startswith='WC')
    a.starting = a.starting.replace(tzinfo=None)
    if a.starting < datetime.datetime.now():

        source_time_zone = pytz.timezone('UTC')
        source_date_with_timezone = source_time_zone.localize(a.starting)
        target_time_zone = pytz.timezone('Asia/Kolkata')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        a.starting = target_date_with_timezone+ datetime.timedelta(days=7)
        a.starting = a.starting.replace(tzinfo=None)
        no = int(a.code[2:])
        no=no+1;
        a.code = "WC"+str(no)
        a.name = "Weekly Contest "+str(no)
        a.link ="https://leetcode.com/contest/weekly-contest-"+str(no)
        a.save()
