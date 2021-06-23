from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

"""
    TO-DO: from csvhandler import views
        The namespace for this urls.py is for the mtgdatabase project
"""

from csvhandler.views import cardimport_upload

from . import views

app_name = 'mtgdatabase'

# urls in templates syntax: {% url 'mtgdatabase:deck' deck.id %}}
# urls for sub-project views: {% url 'csvupload:card' deck.id %}

urlpatterns = [
        # ex: /mtgdatabase/
        path('', views.index, name='index'),
        # ex: /mtgdatabase/deck/#/
        path('deck/<int:deck_id>/', views.deck, name='deck'),
        # ex: /mtgdatabase/card/#/
        path('card/<int:card_id>/', views.card, name='card'),
        # ex: /mtgdatabase/wishlist/#/
        path('wishlist/<int:wishlist_id>/', views.wishlist, name='wishlist'),
        # ex: /mtgdatabase/con_deck/#/#/
        path('con_deck/<int:deck_id>/<int:decklist_id>', views.constructed_deck, name='con_deck'),
        # ex: /mtgdatabase/wishlist_deck/#/#/
        path('wishlist_deck/<int:deck_id>/<int:decklist_id>', views.wishlist_deck, name='wish_deck'),
        path('editcard/<int:card_id>', views.edit_card, name='edit_card'),
        path('upload/', cardimport_upload, name='card upload'),
] 