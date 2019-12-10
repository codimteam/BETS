from django.contrib import admin
from .models import Categories, Matches, Bets, UserProfile, News, Payments, Bets_history, Played_Matches

admin.site.register(Categories)
admin.site.register(Matches)
admin.site.register(Bets)
admin.site.register(UserProfile)
admin.site.register(News)
admin.site.register(Payments)
admin.site.register(Bets_history)
admin.site.register(Played_Matches)