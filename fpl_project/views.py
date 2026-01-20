from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """
    School Fantasy Football League home page.
    Displays landing page with information about the league and encourages students to join.
    """
    return render(request, 'home.html')
