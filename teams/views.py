from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Club, UserTeam, Transfer
from .forms import PlayerSelectionForm
from players.models import Player, POSITION_CHOICES


def teams_index(request):
    clubs = Club.objects.all()
    user_teams = UserTeam.objects.select_related('owner').all()
    return render(request, 'teams/index.html', {'clubs': clubs, 'user_teams': user_teams})


@login_required
def create_team(request):
    """Create a new team for the user"""
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        if team_name:
            team = UserTeam.objects.create(owner=request.user, name=team_name)
            return redirect('teams:manage_players', pk=team.pk)
    
    return render(request, 'teams/create_team.html')


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
    
    # Organize players by position
    gk = team.players.filter(position=1)
    def_players = team.players.filter(position=2)
    mid_players = team.players.filter(position=3)
    fwd_players = team.players.filter(position=4)
    
    # Calculate totals
    gk_count = gk.count()
    def_count = def_players.count()
    mid_count = mid_players.count()
    fwd_count = fwd_players.count()
    
    # Determine formation string
    formation = f"{def_count}-{mid_count}-{fwd_count}"
    
    # Get user's leagues if logged in
    user_leagues = []
    if request.user.is_authenticated:
        user_leagues = request.user.leagues.all()
    
    context = {
        'team': team,
        'gk': gk,
        'def_players': def_players,
        'mid_players': mid_players,
        'fwd_players': fwd_players,
        'gk_count': gk_count,
        'def_count': def_count,
        'mid_count': mid_count,
        'fwd_count': fwd_count,
        'formation': formation,
        'user_leagues': user_leagues,
    }
    return render(request, 'teams/team_detail.html', context)


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

    # Calculate club counts for each player
    player_club_counts = {}
    for player in players:
        if player.team:
            count = team_players.filter(team=player.team).count()
            player_club_counts[player.id] = count
        else:
            player_club_counts[player.id] = 0

    if request.method == 'POST':
        form = PlayerSelectionForm(request.POST, team=team)
        if form.is_valid():
            player = form.cleaned_data['player']
            
            # Check if this is a transfer (replacing someone) or just adding
            existing_position_count = team_players.filter(position=player.position).count()
            position_limit = {1: 1, 2: 4, 3: 3, 4: 3}.get(player.position, 0)
            
            if existing_position_count >= position_limit:
                # This is a transfer - need to check 2 transfer limit
                if not team.can_make_transfer():
                    messages.error(request, f"❌ Transfer limit reached! You can only make 2 transfers per gameweek. Current: {team.get_gameweek_transfers()}/2")
                    return redirect('teams:manage_players', pk=pk)
                messages.info(request, f"⚠️ Transfer being made! Transfers used this gameweek: {team.get_gameweek_transfers() + 1}/2")
            
            team.players.add(player)
            messages.success(request, f"✓ {player.web_name} added to squad!")
            return redirect('teams:manage_players', pk=pk)
    else:
        form = PlayerSelectionForm(team=team)

    # Prepare player list with club count info
    players_with_counts = []
    for player in players:
        players_with_counts.append({
            'player': player,
            'club_count': player_club_counts.get(player.id, 0),
            'can_add': player_club_counts.get(player.id, 0) < 3
        })

    context = {
        'team': team,
        'players': players_with_counts,
        'form': form,
        'position_choices': POSITION_CHOICES,
        'position_counts': position_counts,
        'position_limits': {1: 1, 2: 4, 3: 3, 4: 3},
        'transfers_used': team.get_gameweek_transfers(),
        'transfers_remaining': 2 - team.get_gameweek_transfers(),
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
    messages.success(request, f"✓ {player.web_name} removed from squad!")
    return redirect('teams:manage_players', pk=team_id)


@login_required
def userteam_join_league(request, pk):
    """Assign team to a league"""
    from leagues.models import League
    team = get_object_or_404(UserTeam, pk=pk)
    
    # Check ownership
    if team.owner != request.user:
        messages.error(request, "You can only manage your own teams.")
        return redirect('teams:team_list')
    
    if request.method == 'POST':
        league_id = request.POST.get('league')
        if league_id:
            try:
                league = League.objects.get(pk=league_id)
                # Only allow joining if user is a member
                if league.members.filter(pk=request.user.pk).exists():
                    team.league = league
                    team.save()
                    messages.success(request, f"✓ {team.name} joined {league.name}!")
                    return redirect('teams:team_detail', pk=team.pk)
                else:
                    messages.error(request, "You must be a member of the league first.")
                    return redirect('teams:join_league', pk=team.pk)
            except League.DoesNotExist:
                messages.error(request, "League not found.")
                return redirect('teams:join_league', pk=team.pk)
        else:
            messages.error(request, "Please select a league.")
            return redirect('teams:join_league', pk=team.pk)
    
    # Get leagues the user is a member of
    user_leagues = request.user.leagues.all()
    context = {
        'team': team,
        'user_leagues': user_leagues,
        'current_league': team.league,
    }
    return render(request, 'teams/join_league.html', context)


@login_required
def userteam_assign_league(request):
    """Direct inline league assignment (no page redirect)"""
    from leagues.models import League
    
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        league_id = request.POST.get('league_id')
        
        if not team_id or not league_id:
            messages.error(request, "Missing team or league ID.")
            return redirect('teams:team_detail', pk=team_id) if team_id else redirect('teams:team_list')
        
        try:
            team = UserTeam.objects.get(pk=team_id, owner=request.user)
            league = League.objects.get(pk=league_id)
            
            if league.members.filter(pk=request.user.pk).exists():
                team.league = league
                team.save()
                messages.success(request, f"✓ {team.name} joined {league.name}!")
            else:
                messages.error(request, "You must be a member of the league first.")
        except UserTeam.DoesNotExist:
            messages.error(request, "Team not found or access denied.")
        except League.DoesNotExist:
            messages.error(request, "League not found.")
        
        return redirect('teams:team_detail', pk=team_id)
    
    return redirect('teams:team_list')
