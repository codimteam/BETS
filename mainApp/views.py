from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
import decimal
import random




def add_to_played_matches(match):
    p_match = Played_Matches.objects.create(categories=match.categories, team1=match.team1, team2=match.team2,slug=match.slug,
                                                win1=match.win1,win2=match.win2,draw=match.draw,game_time=match.game_time,
                                                game_end=match.game_end,status=match.status,winner=match.winner)
    p_match.save()


def add_to_bets_history(bet,user,played_match):
    bet_user = Bets_history.objects.create(user = user, match=played_match, choice=bet.choice, coefficient=bet.coefficient,
                                           bet_cash=bet.bet_cash, possible_win=bet.possible_win, bet_date=bet.bet_date,
                                           winner=bet.winner)
    bet_user.save()



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
                bet.save()
                user = User.objects.get(username=bet.client)
                client = UserProfile.objects.get(user=user)
                if bet.choice == bet.winner:
                    client.balance += decimal.Decimal(bet.possible_win)
                    client.save()
                    add_to_played_matches(match)
                    played_match = Played_Matches.objects.all().order_by('-pk')[0]
                    add_to_bets_history(bet,user,played_match)
                    match.delete()
                    bet.delete()
                else:
                    add_to_played_matches(match)
                    played_match = Played_Matches.objects.order_by('-pk')[0]
                    add_to_bets_history(bet, user, played_match)
                    match.delete()
                    bet.delete()

        else:
            if match.game_time < timezone.now() < match.game_end:
                status = 'GOING'
                match.status = status
                match.save()


def index(request):
    allcategories = Categories.objects.all()
    allmatches = Matches.objects.all().order_by('game_time')
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
        change_match_status(matches=allmatches)
    else:
        user_p = 'U should login.'
    allnews = News.objects.all()


    context = {'categories': allcategories,
               'allmatches': allmatches,
               'allnews': allnews,
               'user_p':user_p
               }

    return render(request, 'mainApp/homePage.html', context)


def news(request):
    categories=Categories.objects.all()
    allnews = News.objects.all()
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    context = {
        'allnews' : allnews,
        'user_p' : user_p,
        'categories':categories}
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
    user_p=UserProfile.objects.get(user=request.user)
    if user_p.balance >= decimal.Decimal(bet_money):
        new_bet = Bets.objects.create(client=request.user.username, match=match, choice=choice,
                                  coefficient=coefficient, bet_cash=bet_money,bet_date=bet_date)
        new_bet.save()
        user_p.balance = decimal.Decimal(user_p.balance) - decimal.Decimal(bet_money)
        user_p.save()
        message='SUCCESS'
    else:
        message='You dont have enough money'

    categories = Categories.objects.all()
    matches = Matches.objects.all()
    allnews = News.objects.all()
    user_p = UserProfile.objects.get(user=request.user)
    allmatches = Matches.objects.all()
    change_match_status(matches=allmatches)
    context = {'categories': categories,
               'matches':matches,
               'allnews': allnews,
               'user_p':user_p,
               'message':message}
    return render(request, 'mainApp/events.html', context)


def mybets(request):
    mybets = Bets.objects.filter(client=request.user.username)
    allnews = News.objects.all()
    allmatches = Matches.objects.all()
    categories=Categories.objects.all()
    bets = Bets_history.objects.filter(user=request.user)
    change_match_status(matches = allmatches)
    if request.user.is_authenticated:
        user_p = UserProfile.objects.get(user=request.user)
    else:
        user_p = 'U should login.'
    context={'mybets':mybets,
             'allnews': allnews,
             'user_p':user_p,
             'bets':bets,
             'categories':categories
             }
    return render(request, 'mainApp/mybets.html', context)


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


def profile(request):
    allnews = News.objects.all()
    allcategories = Categories.objects.all()
    allmatches = Matches.objects.all().order_by('game_time')
    user = UserProfile.objects.get(user=request.user)
    context = {'categories': allcategories,
               'allmatches': allmatches,
               'allnews': allnews,
               'user_p': user
               }
    change_match_status(matches=allmatches)
    return render(request,'accounts/profile.html',context)























