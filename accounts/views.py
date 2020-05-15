from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from .models import UserProfile
from django.views import generic
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import UserCreateForm,UserProfileCreateForm
from friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required,user_passes_test

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')



class ProfileView(LoginRequiredMixin,generic.TemplateView):

    template_name = 'accounts/profile.html'

# @login_required
# @user_passes_test(condition)
# def ProfileView(request):
    # pass

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
    success_url = reverse_lazy('profile')
    # def form_valid(self,form):
    #     form.save()
    #     self.request.user.username  = self.request.POST['username']
    #     self.request.user.first_name = self.request.POST['firstname']
    #     self.request.user.last_name = self.request.POST['lastname']
    #     self.request.user.save()
    #     return redirect(self.success_url)
    def get_object(self):
        return self.request.user.profile
