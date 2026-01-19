from django.shortcuts import render, get_object_or_404
from .models import Player


def player_list(request):
    players = Player.objects.select_related('team').all()[:200]
    return render(request, 'players/list.html', {'players': players})


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'players/detail.html', {'player': player})
from django.shortcuts import render

# Create your views here.
