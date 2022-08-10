from django.db import models
from django.contrib.auth.models import User

import os







class GameCategory(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return f'{self.name}'


def game_image( filename, instanse):  
	game_string = filename.name.replace(' ', '')
	return os.path.join(f'photos_{game_string}',instanse)

class Game(models.Model):
	name = models.CharField(max_length=255)
	logo = models.ImageField(
		upload_to = game_image,
		unique=True
		)
	categors = models.ForeignKey(GameCategory, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.name}'


def rank_image(filename, instanse):
	game_string = filename.name.replace(' ', '')
	return os.path.join(f'photos_{game_string}/rank{filename.lvl}', instanse)


class Rank(models.Model):
	name = models.CharField(max_length=255)
	lvl = models.IntegerField()
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ranks')

	img = models.ImageField(
		upload_to=rank_image,
		unique=True
		)

	class Meta:
		ordering = ['-game', '-lvl', '-pk']
	def __str__(self):
		return f'{self.name}'

class Player(models.Model):
	nick = models.CharField(max_length=255)
	birth = models.DateTimeField()
	user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
	ranking = models.ManyToManyField(Rank, related_name='players_count')

	def __str__(self):
		return f'{self.nick}'



class Time(models.Model):
	name = models.CharField(max_length=255)
	instagram = models.CharField(blank=True,null=True,max_length=255)
	twitter	  = models.CharField(blank=True,null=True,max_length=255)
	youtube	  = models.CharField(blank=True,null=True,max_length=255)
	email = models.EmailField(max_length=255)
	phone = models.IntegerField(blank=True,null=True)
	admin = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='proprietario')
	players = models.ManyToManyField(Player, related_name='times')
	ranking = models.IntegerField(default=0)
	
	def __str__(self):
		return f'{self.name}'
	class Meta:
		ordering = ['-ranking', '-pk']




from datetime import datetime
class PlayerConvit(models.Model):
	time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='inscrisoes')
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	is_ingrece = models.BooleanField(default=False)
	send = models.DateTimeField(auto_now_add=True)
	acept = models.DateTimeField(auto_now_add=True)
	to_player = models.BooleanField(default=True)
	kick = models.BooleanField(default=False)
	def __str__(self):
		if self.to_player:
			return f'{self.time.name} invit {self.player.nick}'
		else:
			return f'{self.player.nick} incrible on {self.time.name}'
	def accept(self):
		self.is_ingrece = True
		self.acept = datetime.now()
		self.time.players.add(self.player)
		self.save()

	def cancel(self):
		self.kick = True
		self.time.players.remove(self.player)
		self.save()



class Batalha(models.Model):
	player1 = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='games_read')
	player2 = models.ForeignKey(Time,  on_delete=models.CASCADE,related_name='games_blue', blank=True)
	winer_id = models.IntegerField(default=0)
def upload_Organization(instanse, filename):
	game_string = instanse.name.replace(' ', '')
	return os.path.join(f'organizador_{game_string}/{instanse.pk}', filename)

class Organization(models.Model):
	name = models.CharField(max_length=255)
	logo = models.ImageField(upload_to=upload_Organization)
	def __str__(self):
		return f'{self.name}'


def championchip_banner(instanse, filename):
	_s = instanse.title.replace(' ', '')
	return os.path.join(f'championchip_{_s}/{instanse.pk}', filename)
	
class ChampionChip(models.Model):
	is_lock = models.BooleanField(default=False)
	title = models.CharField(max_length=255)
	subtitle = models.CharField(max_length=255)
	games = models.ManyToManyField(Batalha, blank= True)
	data = models.DateTimeField(auto_now_add=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE , related_name='championchip')
	start = models.DateTimeField()
	organiz = models.ManyToManyField(Organization, blank=True )
	banner = models.ImageField(upload_to=championchip_banner, null=True)
	def __str__(self):
		return f'{self.title}'

	def get_users(self):
		if self.in_game:
			return len(self.in_game.all())
		return 0


class Inscrisao(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	time   = models.ForeignKey(Time, on_delete=models.CASCADE, blank=True)
	championchip = models.ForeignKey(ChampionChip, on_delete=models.CASCADE, related_name='in_game')
	def __str__(self):
		return f'{self.player}'
