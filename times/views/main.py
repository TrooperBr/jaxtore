from django.shortcuts import render, redirect
from django.views import View
from times.models import PlayerConvit, ChampionChip, Time, Player
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from times.forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic.list import ListView
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

def test(request):
	return render(request, 'core/test.html')

def home(request):
	return render(request, 'times/home.html')

def makeChampiomchip(request):
	form = ChampionChipForm(request.POST)
	a = ChampionChip
	return {}



def consumer_championChipsTables(_id):
	context = {}
	_object = ChampionChip.objects.filter(pk=_id)
	c_number = _object.in_game.objects.all().count()/2
	for i in range(_object.count()/2):
		context[i] = [_object.in_game.objects.filter(i),_object.in_game.objects.filter(i*2)]


class MyBaseView(View):
	def get_context_base(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			if Player.objects.filter(user=self.request.user).exists():
				player = Player.objects.get(user=self.request.user)
			else:
				player = False
		else:
			player = False
		context_base = {
			'player':player,
			'basic_info':{
				"ChampionChip":ChampionChip.objects.all(),
			},
			'champs':ChampionChip.objects.all(),
		}
		return context_base


	def post(self):
		return HttpResponse()

	def get(self, *args, **kwargs): #init
		return HttpResponse()






class SearchPlayers(MyBaseView):
	pass



class UserRegister(MyBaseView):
	def post(self, *args, **kwargs):
		form = NewUserForm(self.request.POST)
		if form.is_valid():
			user = form.save()
			login(self.request, user)
			messages.success(self.request, "Registration successful." )
			return redirect("times:player-register")
		messages.error(self.request, "Unsuccessful registration. Invalid information.")
		return redirect("times:register")

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			if Player.objects.filter(user=self.request.user).exists():
				return redirect('times:home')
			else:
				return redirect('times:player-register')
		form = NewUserForm()
		return render(request=self.request, template_name="core/register.html", context={"register_form":form})





class UserLogin(MyBaseView):


	def post(self, *args, **kwargs):
		form = AuthenticationForm(self.request, data=self.request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(self.request, user)
				messages.info(self.request, f"You are now logged in as {username}.")
				return redirect("times:home")
			else:
				messages.error(self.request,"Invalid username or password.")
		else:
			messages.error(self.request,"Invalid username or password.")


	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('times:home')
		form = AuthenticationForm()
		return render(request=self.request, template_name="core/login.html", context={"login_form":form})




from times.forms import PlayerForm
import json


class PlayerRegister(MyBaseView):
	def post(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			if self.request.is_ajax() and \
					'' != self.request.POST['nick'] and \
					'' != self.request.POST['birth']:
				if Player.objects.filter(user=self.request.user).exists():
					return HttpResponse(200)
				print(self.request.POST['nick'])
				Player(
						nick = self.request.POST['nick'],
						birth = self.request.POST['birth'],
						user = self.request.user
				).save()
				messages.success(self.request, "Registration successful." )
				return HttpResponse(json.dumps({
						'successful':True,
						'url':reverse('times:home')
					}))
			return HttpResponse(json.dumps({
						'successful':False,
						'url':reverse('times:home')
					}))
			messages.error(self.request, "Unsuccessful registration. Invalid information.")
			return redirect("times:player-register")

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			form = PlayerForm()
			return render (request=self.request, template_name="core/player_register.html", context={"register_form":form})
		return redirect("times:register")


def viewlogout(request):
	logout(request)
	return redirect('times:home')


class TimeSearch(ListView, MyBaseView):
	model = Time
	template_name = 'teams/teams.html'


	def get_context_base(self, *args, **kwargs):

		context = super().get_context_base(*args, *kwargs)
		context['self_times'] = self.request.user.player.times.all()

		return context

	def post(self, *args, **kwargs):
		return HttpResponse(200)

	def get(self, *args, **kwargs):
		print(self.get_context_base())
		return super().get(*args, **kwargs)



class TimeProfile(DetailView, MyBaseView):
	model = Time
	template_name = 'teams/team.html'



	def get_context_invitation(self):
		context = self.get_context_base()
		if 'player' in context.keys():
			print(context['player'])
			if PlayerConvit.objects.filter(
				player=context['player'], 
				time=Time.objects.get(pk=self.kwargs['pk']),
				kick=False
				).exists():
				context['invit'] = PlayerConvit.objects.get(
					player=context['player'], 
					time=Time.objects.get(pk=self.kwargs['pk']), 
					kick=False
				)
			else:
				context['invit'] = False
		else:
			context['invit'] = False
		return context

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data()
		context.update(self.get_context_invitation())	
		print(context)
		print(context['invit'])
		return context

	def post(self, *args, **kwargs):
		self.object = self.get_object()
		if self.request.user.is_authenticated != True:
			return redirect('times:register')
		if Player.objects.filter(user=self.request.user).exists() != True:
			return redirect('times:player-register')
		context = self.get_context_data()
		if 'invit' in context.keys():
			print('invit exists')
			if context['invit']:
				if context['invit'].is_ingrece:
					context['invit'].cancel()
					print('saiu do time')
				else:
					if context['invit'].to_player:
						print('aceitou o convite')
						context['invit'].accept()
					else:
						print('canselou a ingrece no time')
						context['invit'].cancel()
			else:
				PlayerConvit(
						time = Time.objects.get(pk=self.kwargs['pk']),
						player= Player.objects.get(user=self.request.user),
						is_ingrece=False,
						to_player=False,
				).save()
				print('inscrevel-se')
		else:
			PlayerConvit(
					time = Time.objects.get(pk=self.kwargs['pk']),
					player= Player.objects.get(user=self.request.user),
					is_ingrece=False,
					to_player=False,
			).save()
			print('inscrevel-se')
		if self.request.is_ajax():
			return JsonResponse(
			{'successful':True}
		)
		else:
			return redirect('times:time-profile', self.kwargs['pk'])
		

	def get(self, *args, **kwargs):

		return super().get(*args, **kwargs)


class PlayerProfile(DetailView, MyBaseView):
	model = Player
	template_name = 'player/profile.html'
	def post(self, *args, **kwargs):
		return super().post()
	def get(self, *args, **kwargs):
		return super().get(*args, **kwargs)


class TimeRegister(MyBaseView):
	def post(self, *args, **kwargs):
		form = NewUserForm(self.request.POST)
		if form.is_valid():
			user = form.save()
			login(self.request, user)
			messages.success(self.request, "Registration successful." )
			return redirect("times:player-register")
		messages.error(self.request, "Unsuccessful registration. Invalid information.")
		return redirect("times:register")

	def get(self, *args, **kwargs):
		form = NewUserForm()
		return render (request=self.request, template_name="core/register.html", context={"register_form":form})


class ChampionShipList(ListView, MyBaseView):
	model = ChampionChip
	template_name = 'games/champs.html'
	def get(self, *args, **kwargs):
		
		return super().get(*args, **kwargs)


class GameHome(MyBaseView):

	def post(self):
		return HttpResponse()
	def get(self, *args, **kwargs): #init
		context = self.get_context_base()
		return render(self.request, 'core/home.html', context)