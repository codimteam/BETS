from django.db import models
from django.db.models.signals import pre_save, post_save
import datetime
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
import decimal


class News(models.Model):
    name = models.CharField(max_length=50, default="",editable=True)
    slug = models.SlugField(default="", blank=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='news_images')
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Categories(models.Model):
    sports = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', default="")
    slug = models.SlugField(default="",blank=True)

    def __str__(self):
        return self.sports

    def get_absolute_url(self):
        return reverse('categories', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender,instance, *args,**kwargs):
    if not instance.slug:
        slug = slugify(instance.sports)
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Categories)




class Matches(models.Model):
    MATCH_STATUS = [
        ('COMPLETED', 'COMPLETED'),
        ('GOING', 'GOING'),
        ('EXPECTED', 'EXPECTED')
    ]
    WINNER = [
        ('w1', 'w1'),
        ('w2', 'w2'),
        ('draw', 'draw'),
        ('UNKNOWN', 'UNKNOWN')
    ]
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    team1 = models.CharField(max_length=200, default="", editable=True)
    team2 = models.CharField(max_length=200, default="", editable=True)
    slug = models.SlugField(default="",blank=True)
    win1 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    win2 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    draw = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    game_time = models.DateTimeField()
    game_end = models.DateTimeField(blank=True)
    status = models.CharField(max_length=10,default='EXPECTED', choices=MATCH_STATUS)
    winner = models.CharField(max_length=5, default='UNKNOWN', choices=WINNER)

    def __str__(self):
        return self.team1 + " vs " + self.team2


def pre_save_match_end(sender,instance,*args,**kwargs):
    if not instance.game_end:
        game_end = instance.game_time + datetime.timedelta(minutes=90)
        instance.game_end = game_end


pre_save.connect(pre_save_match_end, sender=Matches)



class Bets(models.Model):
    client = models.CharField(max_length=20,default="",editable=True)
    match = models.ForeignKey(Matches, on_delete=models.CASCADE)
    choice = models.CharField(max_length=5,default="",editable=True)
    coefficient = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    bet_cash = models.DecimalField(max_digits=9,decimal_places=2, default=0.00)
    possible_win = models.DecimalField(max_digits=9,decimal_places=2,default="")
    bet_date = models.DateTimeField()
    winner = models.CharField(max_length=5, default="UNKNOWN", editable=True)

    def __str__(self):
        return self.client +': '+self.match.team1 + " vs " + self.match.team2


def pre_save_possible_win(sender,instance, *args,**kwargs):
    if not instance.possible_win:
        possible_win = decimal.Decimal(instance.bet_cash) * decimal.Decimal(instance.coefficient)
        instance.possible_win = possible_win


pre_save.connect(pre_save_possible_win, sender=Bets)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=20,default="city", editable=True)
    birth_date = models.DateField(null=True,blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2,default=0.0)

    def __str__(self):
        return 'Profile: ' + self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default="")
    card_name = models.CharField(max_length=30, blank=True, default="")
    card_number = models.CharField(max_length=19,blank=True,default="")
    exp_date = models.CharField(max_length=30, blank=True,default="")
    cvv = models.IntegerField(blank=True, default="")
    payment_date = models.DateTimeField()

    def __str__(self):
        return 'Payed-' + self.user.username





