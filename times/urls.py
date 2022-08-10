from django.urls import path
import times.views as views

app_name='times'


urlpatterns = [
    path('', views.GameHome.as_view(), name='home'),
    path('search/players/', views.SearchPlayers.as_view(), name= 'search_players'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('register/player/', views.PlayerRegister.as_view(), name='player-register'),
    path('time/<int:pk>/', views.TimeProfile.as_view(), name='time-profile'),
    path('times/register/', views.TimeRegister.as_view(), name='register-time'),
    path('times/', views.TimeSearch.as_view(), name="search_times"),
    path('player/<int:pk>/' , views.PlayerProfile.as_view(), name='player'),
    path('test/', views.test, name='KNJasjaxdhkJKJASDjasdjhAUQRQYZN'),
    path('logout/', views.viewlogout, name='logout'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('campeonatos/', views.ChampionShipList.as_view() , name='champs'),
    path('ajax/time-register-form' ,views.TimeRegisterFormAjax.as_view(), name='time-register-form-ajax'),
    path('ajax/time-register' ,views.TimeRegisterAjax.as_view(), name='time-register-ajax')

]
