from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Player, POSITION_CHOICES


def player_list(request):
    players = Player.objects.select_related('team').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        players = players.filter(
            Q(web_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(team__name__icontains=search_query)
        )
    
    # Filter by position
    position = request.GET.get('position', '')
    if position:
        players = players.filter(position=position)
    
    # Filter by price range
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    if price_min:
        players = players.filter(now_cost__gte=float(price_min))
    if price_max:
        players = players.filter(now_cost__lte=float(price_max))
    
    # Filter by form (current points)
    form_min = request.GET.get('form_min', '')
    form_max = request.GET.get('form_max', '')
    if form_min:
        players = players.filter(total_points__gte=int(form_min))
    if form_max:
        players = players.filter(total_points__lte=int(form_max))
    
    # Sort
    sort_by = request.GET.get('sort', '-total_points')
    players = players.order_by(sort_by)
    
    context = {
        'players': players[:200],
        'search_query': search_query,
        'position_choices': POSITION_CHOICES,
        'selected_position': position,
        'price_min': price_min,
        'price_max': price_max,
        'form_min': form_min,
        'form_max': form_max,
        'sort_by': sort_by,
    }
    return render(request, 'players/list.html', context)


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'players/detail.html', {'player': player})
