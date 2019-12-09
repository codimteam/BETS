from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
import decimal
import random


def change_match_status(matches):
    choices = ["w1","w2","draw"]
    for match in matches:
        if timezone.now() >= match.game_end:
            status = 'COMPLETED'
            match.status = status
            winner = random.choice(choices)
            match.winner = winner
            match.save()
            bets = Bets.objects.filter(match=match)
            for bet in bets:
                bet.winner = match.winner
                user = User.objects.get(username=bet.client)
                client = UserProfile.objects.get(user=user)
                if bet.choice == bet.winner:
                    client.balance += decimal.Decimal(bet.possible_win)
                    client.save()
        else:
            if match.game_time < timezone.now() < match.game_end:
                status = 'GOING'
                match.status = status
                match.save()


def index(request):
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    allnews = News.objects.all()
    allcategories = Categories.objects.all()
    allmatches = Matches.objects.all().order_by('game_time')
    context = {'categories': allcategories,
               'allmatches': allmatches,
               'allnews': allnews,
               'user_p':user_p
               }
    change_match_status(matches=allmatches)
    return render(request, 'mainApp/homePage.html', context)


def news(request):
    allnews = News.objects.all()
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    context = {
        'allnews' : allnews,
         'user_p' : user_p}
    return render(request, 'mainApp/news.html', context)


def categories(request, category_slug):
    allnews = News.objects.all()
    categories = Categories.objects.all()
    category = Categories.objects.get(slug=category_slug)
    matches = Matches.objects.filter(categories=category)
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    context = {'matches':matches,
               'categories': categories,
               'category':category,
               'allnews': allnews,
               'user_p':user_p}
    return render(request, 'mainApp/events.html', context)


def add_to_cart(request):
    if request.method=="POST":
        match_id=request.POST.get('ev_id')
        choice=request.POST.get('choice')
        coefficient=request.POST.get('coff')
        bet_money=request.POST.get('cash')

    match=Matches.objects.get(pk=match_id)
    bet_date = timezone.now()
    new_bet = Bets.objects.create(client=request.user.username, match=match, choice=choice,
                                  coefficient=coefficient, bet_cash=bet_money,bet_date=bet_date)
    new_bet.save()
    user_p = UserProfile.objects.get(user=request.user)
    user_p.balance = decimal.Decimal(user_p.balance)-decimal.Decimal(bet_money)
    user_p.save()
    categories = Categories.objects.all()
    matches = Matches.objects.all()
    allnews = News.objects.all()
    user_p = UserProfile.objects.get(user=request.user)
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    context = {'categories': categories,
               'matches':matches,
               'allnews': allnews,
               'user_p':user_p}
    return render(request, 'mainApp/events.html', context)


def mybets(request):
    mybets = Bets.objects.filter(client=request.user.username)
    allnews = News.objects.all()
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    context={'mybets':mybets,
             'allnews': allnews,
             'user_p':user_p}
    return render(request,'mainApp/mybets.html',context)


def payment_system(request):
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    context ={
        'user_p' : user_p
    }
    return render(request, 'mainApp/pay.html',context)


def add_on_balance(request):
    if request.method == "POST":
        cash = request.POST.get('cash')
        card_name = request.POST.get('cardname')
        card_number = request.POST.get('cardnumber')
        exp_month = request.POST.get('expmonth')
        exp_year = request.POST.get('expyear')
        cvv = request.POST.get('cvv')
    exp_date = exp_month + '/' + exp_year
    payment_date = timezone.now()
    payment = Payments.objects.create(user=request.user, cash=cash, card_name=card_name,
                                      card_number=card_number,exp_date=exp_date,cvv=cvv, payment_date=payment_date)
    payment.save()
    user = UserProfile.objects.get(user=request.user)
    user.balance += decimal.Decimal(cash)
    user.save()
    success='Your payment was successfully completed. Bet on your pleasure.'
    context={'success':success,
             'user_p':user}
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    return render(request,'mainApp/pay.html', context)























