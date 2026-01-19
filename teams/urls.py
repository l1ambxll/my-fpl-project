from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.teams_index, name='index'),
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('user-teams/', views.userteam_list, name='team_list'),
    path('user-teams/<int:pk>/', views.userteam_detail, name='team_detail'),
    path('user-teams/<int:pk>/manage/', views.userteam_manage_players, name='manage_players'),
    path('user-teams/<int:team_id>/remove-player/<int:player_id>/', views.userteam_remove_player, name='remove_player'),
]
