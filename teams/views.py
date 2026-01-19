from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Club, UserTeam
from .forms import PlayerSelectionForm
from players.models import Player, POSITION_CHOICES


def teams_index(request):
    clubs = Club.objects.all()
    user_teams = UserTeam.objects.select_related('owner').all()
    return render(request, 'teams/index.html', {'clubs': clubs, 'user_teams': user_teams})


def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'teams/club_list.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    return render(request, 'teams/club_detail.html', {'club': club})


def userteam_list(request):
    teams = UserTeam.objects.select_related('owner').all()
    return render(request, 'teams/team_list.html', {'teams': teams})


def userteam_detail(request, pk):
    team = get_object_or_404(UserTeam, pk=pk)
    return render(request, 'teams/team_detail.html', {'team': team})


@login_required
def userteam_manage_players(request, pk):
    team = get_object_or_404(UserTeam, pk=pk)
    
    # Check ownership
    if team.owner != request.user:
        return redirect('teams:team_list')

    # Get filter parameters
    position_filter = request.GET.get('position')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_points = request.GET.get('min_points')

    # Start with all players not in this team
    players = Player.objects.exclude(userteam=team)

    # Apply filters
    if position_filter:
        players = players.filter(position=int(position_filter))
    if min_price:
        players = players.filter(now_cost__gte=float(min_price))
    if max_price:
        players = players.filter(now_cost__lte=float(max_price))
    if min_points:
        players = players.filter(total_points__gte=int(min_points))

    # Calculate position counts in team
    team_players = team.players.all()
    position_counts = {
        1: team_players.filter(position=1).count(),  # GK
        2: team_players.filter(position=2).count(),  # DEF
        3: team_players.filter(position=3).count(),  # MID
        4: team_players.filter(position=4).count(),  # FWD
    }

    if request.method == 'POST':
        form = PlayerSelectionForm(request.POST, team=team)
        if form.is_valid():
            player = form.cleaned_data['player']
            team.players.add(player)
            return redirect('teams:manage_players', pk=pk)
    else:
        form = PlayerSelectionForm(team=team)

    context = {
        'team': team,
        'players': players,
        'form': form,
        'position_choices': POSITION_CHOICES,
        'position_counts': position_counts,
        'position_limits': {1: 1, 2: 4, 3: 3, 4: 3},
        'filters': {
            'position': position_filter,
            'min_price': min_price,
            'max_price': max_price,
            'min_points': min_points,
        }
    }
    return render(request, 'teams/manage_players.html', context)


@login_required
def userteam_remove_player(request, team_id, player_id):
    team = get_object_or_404(UserTeam, pk=team_id)
    
    # Check ownership
    if team.owner != request.user:
        return redirect('teams:team_list')

    player = get_object_or_404(Player, pk=player_id)
    team.players.remove(player)
    return redirect('teams:manage_players', pk=team_id)
