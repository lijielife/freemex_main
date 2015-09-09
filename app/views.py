from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app import models

from googlefinance import getQuotes
# Create your views here.

def updatePrices():
    for i in models.Stock.objects.all():
        i.price=float(getQuotes(i.code)[0]["LastTradePrice"])
        i.save()

def index(request):
    user=request.user
    if user.is_authenticated():
        return HttpResponseRedirect('/portfolio')
    return render(request, 'index_page.html', {})

@login_required
def portfolio(request):
    player = models.Player.objects.get(user_id=request.user.pk)
    return render(request, 'portfolio.html' , {'player': player })

@login_required
def marketwatch(request):
    updatePrices()
    stocks = models.Stock.objects.all()
    return render(request,'marketwatch.html', { 'stocks': stocks })

@login_required
def ranking(request):
    return

@login_required
def stock(request,param):
    return

def rules(request):
    return render(request,'rules.html',{})

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