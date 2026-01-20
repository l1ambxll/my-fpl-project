from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

from .models import League
from .forms import LeagueCreateForm
from django.db.models import Sum
from teams.models import UserTeam


def league_list(request):
    # Get filter parameter
    league_type_filter = request.GET.get('type')
    year_group_filter = request.GET.get('year_group')
    
    leagues = League.objects.select_related('owner').all()
    
    # Apply filters
    if league_type_filter:
        leagues = leagues.filter(league_type=league_type_filter)
    if year_group_filter:
        leagues = leagues.filter(year_group=year_group_filter)
    
    # Organize by type for display
    whole_school_leagues = leagues.filter(league_type='whole_school')
    year_group_leagues = leagues.filter(league_type='year_group').order_by('year_group')
    class_leagues = leagues.filter(league_type='class')
    other_leagues = leagues.filter(league_type='other')
    
    context = {
        'leagues': leagues,
        'whole_school_leagues': whole_school_leagues,
        'year_group_leagues': year_group_leagues,
        'class_leagues': class_leagues,
        'other_leagues': other_leagues,
        'league_type_filter': league_type_filter,
        'year_group_filter': year_group_filter,
    }
    return render(request, 'leagues/list.html', context)


def league_detail(request, slug):
    league = get_object_or_404(League, slug=slug)
    is_member = request.user.is_authenticated and league.members.filter(pk=request.user.pk).exists()
    return render(request, 'leagues/detail.html', {'league': league, 'is_member': is_member})


@login_required
def league_create(request):
    if request.method == 'POST':
        form = LeagueCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            about = form.cleaned_data['about']
            league_type = form.cleaned_data['league_type']
            year_group = form.cleaned_data.get('year_group') or None
            
            slug = slugify(name)
            # ensure unique slug
            base_slug = slug
            counter = 1
            while League.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            league = League.objects.create(
                name=name,
                slug=slug,
                owner=request.user,
                about=about,
                league_type=league_type,
                year_group=year_group
            )
            league.members.add(request.user)
            messages.success(request, f'{league.get_league_type_display()} league "{name}" created successfully.')
            return redirect('leagues:detail', slug=league.slug)
    else:
        form = LeagueCreateForm()

    return render(request, 'leagues/create.html', {'form': form})


@login_required
def league_join(request, slug):
    league = get_object_or_404(League, slug=slug)
    if league.members.filter(pk=request.user.pk).exists():
        messages.info(request, 'You are already a member of this league.')
        return redirect('leagues:detail', slug=slug)

    league.members.add(request.user)
    messages.success(request, f'You have joined {league.name}.')
    return redirect('leagues:detail', slug=slug)


def league_leaderboard(request, slug):
    league = get_object_or_404(League, slug=slug)
    # Teams assigned to this league
    teams = (
        UserTeam.objects.filter(league=league)
        .annotate(score=Sum('players__total_points'))
        .order_by('-score')
    )
    return render(request, 'leagues/leaderboard.html', {'league': league, 'teams': teams})

