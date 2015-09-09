from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app import models

# Create your views here.

def index(request):
    user=request.user
    if user.is_authenticated():
        return HttpResponseRedirect('/portfolio')
    return render(request, 'index_page.html', {})

def portfolio(request):
    player = models.Player.objects.get(user_id=request.user.pk)
    print (player.name)
    return render(request, 'portfolio.html' , {'player': player})

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.email = user.email
            player.name = response.get('name')
            player.save()

    elif backend.name == 'google-oauth2':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.email = user.email
            player.name = response.get('name')['givenName'] + " " + response.get('name')['familyName']
            player.save()