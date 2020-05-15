from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from .models import UserProfile
from django.views import generic
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import UserCreateForm,UserProfileCreateForm
from friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')



# class ProfileView(LoginRequiredMixin,generic.TemplateView):

    # template_name = 'accounts/profile.html'

@login_required
# @user_passes_test(condition)
def get_profile(request,username):
    user_profile = User.objects.get(username=username)
    # List all of a user's friends:
    friend_list = Friend.objects.friends(request.user)
    # List all unread friendship requests:
    friend_requests_unread = Friend.objects.unread_requests(user=request.user)
    # List all unrejected friendship requests:
    friend_requests = Friend.objects.unrejected_requests(user=request.user)
    # Count of all unrejected friendship requests:
    friend_requests_count = Friend.objects.unrejected_request_count(user=request.user)
    # List all rejected friendship requests:
    friend_requests_rejected = Friend.objects.rejected_requests(user=request.user)
    # Count of all rejected friendship requests:
    # friend_requests_rejected_count = Friend.objects.rejected_request_count(user=request.user)
    # List of all sent friendship requests:
    friend_requests_sent = Friend.objects.sent_requests(user=request.user)
    # Test if two users are friends:
    # Friend.objects.are_friends(request.user, other_user) == True
    if request.user.username==username:
        visitor= False
    else:
        visitor = True
    context = {
                'visitor':visitor,
                'user_profile':user_profile,
                'friend_list':friend_list,
                'friend_requests_unread':friend_requests_unread,
                'friend_requests':friend_requests,
                'friend_requests_count':friend_requests_count,
                'friend_requests_rejected':friend_requests_rejected,
                # 'friend_requests_rejected_count':friend_requests_rejected_count,
                'friend_requests_sent':friend_requests_sent,

              }
    return render(request,'accounts/profile.html',context)



class CreateProfileView(LoginRequiredMixin,generic.UpdateView):
    model = UserProfile
    form_class = UserProfileCreateForm
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('index')

    # def form_valid(self,form):
    #     form.save()
    #     # self.request.user.username  = self.request.POST['username']
    #     # self.request.user.first_name = self.request.POST['firstname']
    #     # self.request.user.last_name = self.request.POST['lastname']
    #     self.request.user.save()
    #     return redirect(self.success_url)
    def get_object(self):
        return self.request.user.profile

class UpdateProfileView(LoginRequiredMixin,generic.UpdateView):
    model = UserProfile
    form_class = UserProfileCreateForm
    template_name = 'accounts/update_profile.html'
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username,})
    # success_url = reverse_lazy('profile',kwargs={'username':get_object()})
    # def form_valid(self,form):
    #     form.save()
    #     self.request.user.username  = self.request.POST['username']
    #     self.request.user.first_name = self.request.POST['firstname']
    #     self.request.user.last_name = self.request.POST['lastname']
    #     self.request.user.save()
    #     return redirect(self.success_url)
    def get_object(self):
        return self.request.user.profile
