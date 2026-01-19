from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('', views.league_list, name='list'),
    path('create/', views.league_create, name='create'),
    path('<slug:slug>/join/', views.league_join, name='join'),
    path('<slug:slug>/leaderboard/', views.league_leaderboard, name='leaderboard'),
    path('<slug:slug>/', views.league_detail, name='detail'),
]
