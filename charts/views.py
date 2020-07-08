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
from operator import itemgetter
import datetime,calendar
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

def comparison(request):
    return render(request, 'charts/comparison.html')

def charts(request):
    return render(request,'charts/charts.html')




def get_data(request):
    data = dict()
    if request.method == 'GET' and request.is_ajax():
        handle = request.GET.get('handle')
        url = 'https://codeforces.com/api/user.status?handle={}&from=1'.format(handle)
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
                for submission in result:
                    if submission['verdict'] in verdicts:
                        verdicts[submission['verdict']] += 1
                    else:
                        verdicts[submission['verdict']] = 1
                    if submission['verdict']=="OK" :
                        user.accepted +=1
                        for y in submission['problem']['tags']:
                            if y in tags:
                                tags[y] +=1
                            else:
                                tags[y] = 1

                        try:
                            prob_rating = submission['problem']['rating']
                            if prob_rating in level:
                                level[prob_rating]+=1
                            else:
                                level[prob_rating]=1
                        except:
                            pass

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
                prob_rating_list = sorted(prob_rating_list,key=itemgetter('rating'),reverse=True)
                user.prob_rating = prob_rating_list
                user.verdicts = verdicts_list
                data['user_data'] = user.__dict__
                data['success'] = True

            else:
                data['success'] = False
        else :
            data['success'] = False
    else:
        data['success'] = False
    # print(data)
    return JsonResponse( data)







def get_both_user_ratings(request):
    data = dict()
    data['success'] = False
    if request.method=='GET' and request.is_ajax():
        username = request.GET.get('handle')
        username2 = request.GET.get('user2_handle')
        url = "https://codeforces.com/api/user.rating?handle={}".format(username)
        url2 = "https://codeforces.com/api/user.rating?handle={}".format(username2)
        r = requests.get(url)
        r2 = requests.get(url2)
        data['status_code'] = r.status_code
        if r.status_code != 200:
            pass
        else:
            json_data = r.json()
            json_data2 = r2.json()
            if json_data['status']!='OK' and  json_data2['status']!='OK':
                pass
            else:
                result1 = json_data['result']
                result2 = json_data2['result']
                contests_list = []
                rating_list = []
                rating_change_list =[]
                rank_list = []
                time_list = []
                line_chart_data_list = []
                contests_list2 = []
                rating_list2 = []
                rating_change_list2 =[]
                rank_list2 = []
                time_list2 = []


                i = 0
                j = 0
                old1 = 1500
                old2 = 1500
                print(len(result1))
                print(len(result2))
                while i<len(result1) and j<len(result2):
                    contest1 = result1[i]
                    contest2 = result2[j]
                    time1 = contest1['ratingUpdateTimeSeconds']
                    time2 = contest2['ratingUpdateTimeSeconds']
                    if time1==time2 :
                        month = datetime.datetime.utcfromtimestamp(time1).month
                        day = datetime.datetime.utcfromtimestamp(time1).day
                        year = datetime.datetime.utcfromtimestamp(time1).year
                        time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)
                        old1 = contest1['newRating']
                        new1 = contest1['newRating']

                        old2 = contest2['newRating']
                        new2 = contest2['newRating']
                        time_list.append(time_str)
                        rating_list.append(new1)
                        rating_list2.append(new2)
                        i=i+1
                        j=j+1
                        line_chart_data_list.append({'date':time_str,'rating1':old1,'rating2':old2,})

                    elif time1<time2:
                        month = datetime.datetime.utcfromtimestamp(time1).month
                        day = datetime.datetime.utcfromtimestamp(time1).day
                        year = datetime.datetime.utcfromtimestamp(time1).year
                        time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)
                        old1 = contest1['newRating']
                        new1 = contest1['newRating']
                        time_list.append(time_str)
                        rating_list.append(new1)
                        rating_list2.append(old2)
                        line_chart_data_list.append({'date':time_str,'rating1':old1,'rating2':old2,})
                        i=i+1

                    else :
                        month = datetime.datetime.utcfromtimestamp(time2).month
                        day = datetime.datetime.utcfromtimestamp(time2).day
                        year = datetime.datetime.utcfromtimestamp(time2).year
                        time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)
                        time_list.append(time_str)
                        old2 = contest2['newRating']
                        new2 = contest2['newRating']
                        line_chart_data_list.append({'date':time_str,'rating1':old1,'rating2':old2,})
                        rating_list.append(old1)
                        rating_list2.append(new2)
                        j=j+1



                if i==len(result1):
                    while j<len(result2):
                        contest2 = result2[j]
                        time2 = contest2['ratingUpdateTimeSeconds']
                        month = datetime.datetime.utcfromtimestamp(time2).month
                        day = datetime.datetime.utcfromtimestamp(time2).day
                        year = datetime.datetime.utcfromtimestamp(time2).year
                        time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)
                        old1 = contest2['newRating']
                        new1 = contest2['newRating']
                        time_list.append(time_str)
                        line_chart_data_list.append({'date':time_str,'rating1':old1,'rating2':old2,})
                        rating_list2.append(old2)
                        rating_list.append(old1)
                        j=j+1

                elif j==len(result2) :
                    while i<len(result1):
                        contest1 = result1[i]
                        time1 = contest1['ratingUpdateTimeSeconds']
                        month = datetime.datetime.utcfromtimestamp(time1).month
                        day = datetime.datetime.utcfromtimestamp(time1).day
                        year = datetime.datetime.utcfromtimestamp(time1).year
                        time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)
                        old1 = contest1['newRating']
                        new1 = contest1['newRating']
                        time_list.append(time_str)
                        line_chart_data_list.append({'date':time_str,'rating1':old1,'rating2':old2,})
                        rating_list2.append(old2)
                        rating_list.append(old1)
                        i=i+1



                """
                for contest in result:
                    contestName = contest['contestName']
                    rank = contest['rank']
                    time = contest['ratingUpdateTimeSeconds']

                    month = datetime.datetime.utcfromtimestamp(time).month
                    day = datetime.datetime.utcfromtimestamp(time).day
                    year = datetime.datetime.utcfromtimestamp(time).year
                    time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)

                    oldRating =contest['oldRating']
                    newRating = contest['newRating']
                    if oldRating == 0:
                        oldRating = 1500
                    ratingChange = newRating-oldRating
                    if ratingChange>0:
                        ratingChange="+"+str(ratingChange)
                    else:
                        ratingChange = str(ratingChange)
                    rating_list.append(newRating)
                    rating_change_list.append(newRating-oldRating)
                    rank_list.append(rank)
                    time_list.append(time_str)
                    contests_list.append(contestName)
                    line_chart_data_list.append({'rating':newRating,'date':time_str,'contestName':contestName,'ratingChange':ratingChange,'rank' :rank,})

                data['rank_list'] =  rank_list
                data['time_list'] = time_list
                data['rating_change_list'] = rating_change_list
                data['contests_list'] = contests_list
                """
                data['line_chart_data_list'] = line_chart_data_list
                data['success'] = True
    print(result2)
    return JsonResponse(data)

















def get_Rating(request) :
    data = dict()
    if request.method == 'GET' and request.is_ajax():
        handle = request.GET.get('handle')
        handle2 = request.GET.get('user2_handle')
        data['handle'] = handle
        data['handle2'] = handle2
        data["ContestId"] = []
        url = "https://codeforces.com/api/user.rating?handle={}".format(handle)
        url2 = "https://codeforces.com/api/user.rating?handle={}".format(handle2)
        r = requests.get(url)
        r2 = requests.get(url2)
        Ratings1 = 0
        Ratings2 = 0
        User1_best_rank = 50000
        User2_best_rank = 50000
        User1_worst_rank = 0
        User2_worst_rank = 0
        #Ratings1 ans 2 are the max ratings of the users
        if r.status_code == 200 and r2.status_code == 200 :
            json_data = r.json()
            json_data2 = r2.json()
            if json_data['status']=="OK" and json_data2['status']=="OK" :
                result1 = json_data["result"]
                result2 = json_data2["result"]
                #recentcontestid1 = 0
                #recentcontestid2 = 0
                All_Ratings1 = []
                All_Ratings2 = []
                Common_cont = []
                #common_cont contains ranks of all the common contests
                #Starting = min(result1[0]['contestId'],result2[0]['contestId'])
                for x in result1 :
                    Ratings1 = max(Ratings1,x["newRating"])
                    User1_best_rank = min(User1_best_rank,x['rank'])
                    User1_worst_rank = max(User1_worst_rank,x['rank'])

                    for y in result2 :
                        if x["contestId"]== y["contestId"]:
                            Common_cont.append([x["rank"],y["rank"]])
                            data["ContestId"].append(x["contestId"])
                    #recentcontestid1 = max(recentcontestid1,x["contestId"])
                    All_Ratings1.append(x["newRating"])
                for x in result2 :
                    User2_best_rank = min(User2_best_rank,x['rank'])
                    User2_worst_rank = max(User2_worst_rank,x['rank'])
                    Ratings2 = max(Ratings2,x["newRating"])
                    #recentcontestid2 = max(recentcontestid2,x["contestId"])
                    All_Ratings2.append(x["newRating"])
                data['success'] = True
                data['Rating1'] = Ratings1
                data['Rating2'] = Ratings2
                data['User1_Ratings'] = All_Ratings1
                data['User2_Ratings'] = All_Ratings2
                MaxContestNo = max(len(result1),len(result2))
                data['Contests'] = []
                data['Common_cont'] = Common_cont
                data['User1_best_rank'] = User1_best_rank
                data['User1_worst_rank'] = User1_worst_rank
                data['User2_best_rank'] = User2_best_rank
                data['User2_worst_rank'] = User2_worst_rank
                for i in range(1,MaxContestNo + 1):
                    data['Contests'].append(i)
                #print(data['Common_cont'])

            else :
                data['success'] = False
        else:
            data['success'] = False
    else:
        data['success'] = False

    return JsonResponse(data)
