from django.shortcuts import render
from django.urls import reverse_lazy
# Create your views here.
from django.views import generic
from . forms import UserCreateForm
class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
