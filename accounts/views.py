from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import *
from mainApp.models import *


def signup_view(request):
    news = News.objects.all()
    categories = Categories.objects.all()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        args = {
            'categories': categories,

            'allnews': news,
            'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
        args = {
            'categories': categories,
            'allnews': news,
            'form': form}
    return render(request, 'accounts/signup.html', args)


def login_view(request):
    news = News.objects.all()
    categories = Categories.objects.all()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
        args = {
                'categories': categories,

                'allnews': news,
                'form':form}
    return render(request, 'accounts/login.html',args)


def logout_view(request):
    if request.method =='POST':
        logout(request)
        return redirect('index')


def edit_profile(request):
    news = News.objects.all()
    categories = Categories.objects.all()
    user_p = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form_user = EditProfileForm(request.POST, instance=request.user)
        form_profile = ProfileForm(request.POST, instance=request.user.userprofile)
        if form_user.is_valid and form_profile.is_valid:
            form_user.save()
            form_profile.save()
            return redirect('profile')
    else:
        form_user = EditProfileForm(request.POST, instance=request.user)
        form_profile = ProfileForm(request.POST, instance=request.user.userprofile)
        args={'form_user':form_user,
              'form_profile': form_profile,
              'categories': categories,
              'user_p':user_p,
              'allnews':news}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    news = News.objects.all()
    categories = Categories.objects.all()
    user_p = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    response = render(request, 'accounts/change_password.html', {
        'form': form
    })
    response.set_cookie('password_changed', 'true')
    return response

