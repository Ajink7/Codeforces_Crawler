from django.shortcuts import render
import webbrowser,bs4,sys,requests
import datetime,calendar
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
        url = 'https://codeforces.com/api/user.status?handle={}&from=1'.format(handle)
        r = requests.get(url)
        if r.status_code==200:
            json_data  = r.json()
            if json_data['status']=='OK':
                result = json_data['result']
                # print(result)
                user = Userdata()
                user.total_submission = len(result)
                user.accepted = 0
                # to get total solved and total tried problems
                solved_probs = set()
                tried_probs = set()
                # to get unsolved problems
                unsolved = []

                solved = []
                level = {}
                tags = {}
                verdicts = {}
                for submission in result:
                    if submission['verdict'] in verdicts:
                        verdicts[submission['verdict']] += 1
                    else:
                        verdicts[submission['verdict']] = 1
                    tried_probs.add(str(submission['problem']['contestId'])+"-"+submission['problem']['index'])
                    if submission['verdict']=="OK" :
                        solved_prob = dict()
                        solved_prob['name'] = str(submission['problem']['contestId'])+"-"+submission['problem']['index']
                        solved_prob['link'] = "https://codeforces.com/contest/{}/problem/{}".format(submission['problem']['contestId'],submission['problem']['index'])
                        if solved_prob not in solved:
                            solved.append(solved_prob)
                        solved_probs.add(str(submission['problem']['contestId'])+"-"+submission['problem']['index'])
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
                    else:
                        unsolved_prob = dict()
                        unsolved_prob['name'] = str(submission['problem']['contestId'])+"-"+submission['problem']['index']
                        unsolved_prob['link'] = "https://codeforces.com/contest/{}/problem/{}".format(submission['problem']['contestId'],submission['problem']['index'])
                        if unsolved_prob not in unsolved:
                            unsolved.append(unsolved_prob)

                unsolved_final = []
                for prob in unsolved:
                    if prob['name'] not in solved_probs:
                        unsolved_final.append(prob)
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

                # user statistics
                data['tried_probs_count']=len(tried_probs)
                data['solved_probs_count']=len(solved_probs)

                # unsolved Problems
                data['unsolved'] = unsolved_final
                data['success'] = True

            else:
                data['success'] = False
        else :
            data['success'] = False
    else:
        data['success'] = False
    # print(data)
    return JsonResponse( data)

def get_user_ratings(request):
    data = dict()
    data['success'] = False
    if request.method=='GET' and request.is_ajax():
        username = request.GET.get('handle')
        url = "https://codeforces.com/api/user.rating?handle={}".format(username)
        r = requests.get(url)
        data['status_code'] = r.status_code
        if r.status_code != 200:
            pass
        else:
            json_data = r.json()
            if json_data['status']!='OK':
                pass
            else:
                result = json_data['result']
                contests_list = []
                rating_list = []
                rating_change_list =[]
                rank_list = []
                time_list = []
                line_chart_data_list = []

                maxrating=0
                minrating=5000
                max_rating_up=0
                max_rating_down=0
                best_rank = pow(10,9)
                worst_rank=1
                contests_count=len(result)

                for contest in result:
                    contestName = contest['contestName']
                    rank = contest['rank']
                    best_rank = min(best_rank,rank)
                    worst_rank = max(worst_rank,rank)
                    time = contest['ratingUpdateTimeSeconds']

                    month = datetime.datetime.utcfromtimestamp(time).month
                    day = datetime.datetime.utcfromtimestamp(time).day
                    year = datetime.datetime.utcfromtimestamp(time).year
                    time_str = calendar.month_abbr[month] + " " + str(day) + " "+str(year)

                    oldRating =contest['oldRating']
                    newRating = contest['newRating']
                    maxrating = max(maxrating,newRating)
                    minrating = min(minrating,newRating)
                    if oldRating == 0:
                        oldRating = 1500
                    ratingChange = newRating-oldRating
                    if(ratingChange>0):
                        max_rating_up = max(max_rating_up,ratingChange)
                    if(ratingChange<0):
                        max_rating_down = min(max_rating_down,ratingChange)
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
                data['line_chart_data_list'] = line_chart_data_list

                # user statistics
                data['maxrating']= maxrating
                data['minrating']= minrating
                data['max_rating_up'] = max_rating_up
                data['max_rating_down'] = max_rating_down
                data['contests_count'] = contests_count
                data['best_rank'] = best_rank
                data['worst_rank'] = worst_rank
                # data collected successfully
                data['success'] = True
    # print(data)
    return JsonResponse(data)
