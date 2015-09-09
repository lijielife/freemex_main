from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app import models

import datetime
from googlefinance import getQuotes
# Create your views here.

updateTime = datetime.datetime.now()
val = False

def updatePrices():
    for i in models.Stock.objects.all():
        i.price=float(getQuotes(i.code)[0]["LastTradePrice"].replace(',',''))
        i.save()

def index(request):
    global updateTime
    if updateTime == None:
        updateTime = datetime.datetime.now()
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
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    stocks = models.Stock.objects.all()
    return render(request,'marketwatch.html', { 'stocks': stocks })

@login_required
def ranking(request):
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    players = models.Player.objects.all()
    if val :
        val = False
        print ("here")
        for p in players:
            p.value_in_stocks=0
            for j in models.PlayerToStock.objects.filter(player=p):
                p.value_in_stocks += j.stock.price
            p.save()
    return render(request,'rankings.html',{'players':players})

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