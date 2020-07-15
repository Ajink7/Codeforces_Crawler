from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
import datetime
from accounts.models import UserProfile
# class IndexView(generic.TemplateView):
#     # print(datetime.datetime.now())
#
#     template_name = 'index.html'

def IndexView(request):
    if request.user.is_authenticated:
        profile,created = UserProfile.objects.get_or_create(user = request.user)

        if created:
            print('created')
            profile.save()
            return redirect('accounts/create_profile/')


    return render(request,'index.html')


def Team(request):
    return render(request,'team.html')
