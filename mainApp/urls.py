from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<category_slug>/', views.categories, name='categories'),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('mybets/', views.mybets, name="mybets"),
    path('news/', views.news,name='news'),
    path('payment_system/',views.payment_system, name='payment_system'),
    path('add_on_balance', views.add_on_balance, name='add_on_balance'),
    path('profile/', views.profile, name='profile'),
]
