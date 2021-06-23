from django.contrib import admin

from .models import Deck, Card, Wishlist, Decklist, ExpansionSet

# Register your models here.

admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(Wishlist)
admin.site.register(Decklist)
admin.site.register(ExpansionSet)