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
    print("======= updating prices ==========")
    for i in models.Stock.objects.all():
        i.price=float(getQuotes(str(i.code))[0]["LastTradePrice"].replace(',',''))
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
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    if val :
        val = False
        print("here")
        playerObj = models.Player.objects.get(user_id=request.user.pk)
        playerObj.value_in_stocks = 0
        for j in models.PlayerToStock.objects.filter(player=playerObj):
            playerObj.value_in_stocks += j.stock.price*j.quantity
            playerObj.save()
    player = models.Player.objects.get(user_id=request.user.pk)
    p2sList = models.PlayerToStock.objects.filter(player = player, quantity__gt = 0)
    return render(request, 'portfolio.html' , {'player': player, 'p2sList': p2sList})

@login_required
def marketwatch(request):
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    stocks = models.Stock.objects.all()
    return render(request,'marketwatch.html', { 'stocks': stocks })

def stockDetails(request):
    stockCode = request.GET['code']
    return render(request,'stockdetails.html', { 'code': stockCode })

@login_required
def buyStock(request):
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    if request.method == 'POST':
        print(request.POST)
        try:
            requestedStockCode = request.POST['stock_code']
            requestedStockCount = int(request.POST['number_of_stocks'])
        except:
            messages.error(request, 'Please select stock and enter quantity')
            stocks = models.Stock.objects.all()
            return render(request,'buy_stock.html', { 'stocks': stocks })
        stockList = models.Stock.objects.filter(code = str(requestedStockCode))
        playerObj = models.Player.objects.get(user_id=request.user.pk)
        availableMoney = float(playerObj.cash)
        if(stockList.count() and (requestedStockCount > 0)):
            stockObj = stockList[0]
            stockPrice = stockObj.price
            print(stockPrice)
            print(requestedStockCount)
            if(availableMoney > (stockPrice * requestedStockCount)):
                print("BOUGHT")
                #update player to stock table
                p2sList = models.PlayerToStock.objects.filter(player = playerObj, stock = stockObj)
                if(p2sList.count()):
                    p2s = p2sList[0]
                    p2s.quantity = p2s.quantity + requestedStockCount
                    p2s.save()
                    print("UPDATED")
                    msg = 'Stock purchased successfully. \n Cash Deducted: ' + str(stockPrice * requestedStockCount)
                    messages.success(request, msg)
                else:
                    p2s = models.PlayerToStock()
                    p2s.player = playerObj
                    p2s.stock = stockObj
                    p2s.quantity = requestedStockCount
                    p2s.save()
                    print("UPDATED")
                    msg = 'Stock purchased successfully. \n Cash Deducted: ' + str(stockPrice * requestedStockCount)
                    messages.success(request, msg)
                #deduct player money
                newAvailableMoney = availableMoney - (stockPrice * requestedStockCount)
                playerObj.cash = newAvailableMoney
                print("CASH DEDUCTED")
                #change player value in stock
                playerObj.value_in_stocks=0
                for j in models.PlayerToStock.objects.filter(player = playerObj):
                    playerObj.value_in_stocks += j.stock.price*j.quantity
                playerObj.save()
            else:
                messages.error(request, 'Not enough cash to buy stock')
        else:
            messages.error(request, 'Something went wrong')

    stocks = models.Stock.objects.all()
    playerObj = models.Player.objects.get(user_id=request.user.pk)
    return render(request,'buy_stock.html', { 'stocks': stocks, 'player': playerObj })

@login_required
def sellStock(request):
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    if request.method == 'POST':
        print(request.POST)
        try:
            requestedStockCode = request.POST['stock_code']
            requestedStockCount = int(request.POST['number_of_stocks'])
        except:
            messages.error(request, 'Please select stock and enter quantity')
            stocks = models.PlayerToStock.objects.filter(quantity__gt = 0)
            return render(request,'sell_stock.html', { 'stocks': stocks })

        playerObj = models.Player.objects.get(user_id=request.user.pk)
        stockList = models.Stock.objects.filter(code = str(requestedStockCode))
        if(stockList.count() and (requestedStockCount > 0)):
            stockObj = stockList[0]
            p2sList = models.PlayerToStock.objects.filter(player = playerObj, stock = stockObj)
            if(p2sList.count()):
                p2s = p2sList[0]
                if(p2s.quantity >= requestedStockCount):
                    #DEDUCT STOCK QUANTITY
                    p2s.quantity = p2s.quantity - requestedStockCount
                    
                    #INCREASE PLAYER CASH
                    playerObj.cash = (playerObj.cash + (requestedStockCount * p2s.stock.price))
                    p2s.save()
                    playerObj.save()
                    print("SOLD")
                    
                    #change player value in stock
                    playerObj.value_in_stocks=0
                    for j in models.PlayerToStock.objects.filter(player = playerObj):
                        playerObj.value_in_stocks += j.stock.price*j.quantity
                    playerObj.save()
                    
                    #set success message
                    messages.success(request, 'Stock sold successfully.')
                else:
                    messages.error(request, 'You dont have that much stock to sell')
            else:
                messages.error(request, 'You have not bought this stock')
        else:
            messages.error(request, 'Something went wrong')
    playerObj = models.Player.objects.get(user_id=request.user.pk)
    stocks = models.PlayerToStock.objects.filter(player = playerObj, quantity__gt = 0)
    return render(request,'sell_stock.html', { 'stocks': stocks })

def ranking(request):
    global updateTime,val
    if datetime.datetime.now()-datetime.timedelta(minutes=1)>=updateTime:
        updateTime=datetime.datetime.now()
        updatePrices()
        val = True
    players = models.Player.objects.all()
    if val :
        val = False
        print("here")
        for p in players:
            p.value_in_stocks=0
            for j in models.PlayerToStock.objects.filter(player=p):
                p.value_in_stocks += j.stock.price*j.quantity
            p.save()
    players= list(players)
    players.sort(key=lambda x: x.cash + x.value_in_stocks, reverse = True)
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