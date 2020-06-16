from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import UserProfile,FriendRequest
from django.views import generic
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import UserCreateForm,UserProfileCreateForm
from friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
#friendship views


def send_friend_request(request):
	if request.method=='GET' and request.is_ajax():
		username = request.GET.get('username',None)
		user = get_object_or_404(User, username = username)
		frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
		sucess = False
		if created or frequest:
			success = True
		data = {
			'success':success
		}
		return JsonResponse(data)
def cancel_friend_request(request):
	if request.method=='GET' and request.is_ajax():
		username = request.GET.get('username',None)
		user = get_object_or_404(User, username=username)
		sucess = False;
		frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user)
		frequest.delete()
		success = True;
		data = {
			'success':success
		}
		return JsonResponse(data)

def accept_friend_request(request, username):
	from_user = get_object_or_404(User, username=username)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return redirect(reverse('profile',kwargs={'username':request.user.username}))

def delete_friend_request(request, username):
	from_user = get_object_or_404(User, username = username)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return redirect(reverse('profile',kwargs={'username':request.user.username}))

def remove_friend(request):
	if request.method=="GET" and request.is_ajax():
		success = False
		username = request.GET.get('username',None)
		to_remove_user = get_object_or_404(User,username = username)
		request.user.profile.friends.remove(to_remove_user.profile)
		to_remove_user.profile.friends.remove(request.user.profile)
		success = True
		data ={
			'success':success
		}
	return JsonResponse(data)

####
class SignUpView(generic.CreateView):
	form_class = UserCreateForm
	template_name = 'accounts/signup.html'
	success_url = reverse_lazy('login')



# class ProfileView(LoginRequiredMixin,generic.TemplateView):

	# template_name = 'accounts/profile.html'

@login_required
def get_profile(request,username):

	u = User.objects.get(username=username)
	p = u.profile
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

	friends = p.friends.all()

	# is this user our friend
	friend_status = 'none'
	if p not in request.user.profile.friends.all():
		friend_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				friend_status = 'friend_request_sent'
	else: friend_status = 'friend'
	context = {
		'u': u,
		'friend_status': friend_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests
	}

	return render(request, "accounts/profile.html", context)



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

class SearchUsers(generic.ListView):
	model = User
	template_name='accounts/search_users.html'
	context_object_name = 'users'
	def get_queryset(self):
		query = self.request.GET.get('query')
		object_list = User.objects.filter(username__icontains=query).exclude(is_superuser = True)
		return object_list

def friend_status(request):
	if request.method == "GET" and request.is_ajax():
		username = request.GET.get('username',None)
		friend_status = None
		u = User.objects.get(username=username)
		p = u.profile
		if p not in request.user.profile.friends.all():
			friend_status = 'not_friend'

			# if we have sent him a friend request
			if len(FriendRequest.objects.filter(
				from_user=request.user).filter(to_user=p.user)) == 1:
					friend_status = 'friend_request_sent'
		else: friend_status = 'friend'

		data={
			'friend_status':friend_status
		}

	return JsonResponse(data)
