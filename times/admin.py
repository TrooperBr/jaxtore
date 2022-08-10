from django.contrib import admin
from .models import (
	Player,
	Rank,
	Game,
	Time,
	PlayerConvit,
	Batalha,
	ChampionChip,
	Inscrisao,
	GameCategory
)
# Register your models here.

admin.site.register(Game)
admin.site.register(Rank)
admin.site.register(Player)
admin.site.register(Time)
admin.site.register(PlayerConvit)
admin.site.register(Batalha)
admin.site.register(ChampionChip)
admin.site.register(Inscrisao)
admin.site.register(GameCategory)