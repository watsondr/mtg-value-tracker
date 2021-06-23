from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from pathlib import Path

from .models import Deck, Decklist, Card, ExpansionSet, Forex
from MTGDeckValueTracker.settings import STATIC_ROOT
import decimal, json, requests

"""
    TO-DO: IMPLEMENT TEMPLATES FOR HTML PAGES
        TO-DO: GET DECK LOADING WHEN MAIN LOADS [DONE 30/01/2021]
    TO-DO: FINISH THE REST OF THE VIEWS
    TO-DO: PUT GLOBAL FUNCTIONS IN SEPERATE FILE AND IMPORT THEM
    TO-CHECK: CAN I IMPORT GLOBAL [[ VARIABLES ]] FROM ANOTHER FILE?
    TO-DO: IMPLEMENT CLASS BASED VIEWS
    TO-DO: ENSURE ALL VIEWS HAVE SITE WIDE NAVIGATION IN THEIR TEMPLATES
"""

# query optimisation: https://docs.djangoproject.com/en/3.0/ref/models/querysets/

# --- DEFINING GLOBAL VARIABLES --- 

# define list of MTG concepts to convert database entries to be human readable

MTG_FORMATS = { 
        'COM' : 'Commander',
        'VNT' : 'Vintage',
        'LEG' : 'Legacy',
        'MOD' : 'Modern',
        'PIO' : 'Pioneer',
        'STD' : 'Standard',
        'PAU' : 'Pauper'
  }

MTG_RARITY = {
        'COM' : 'Common',
        'UCO' : 'Uncommon',
        'RAR' : 'Rare',
        'MYC' : 'Mythic'
  }

MTG_CARDTYPE = {
        'CTR' : 'Creature',
        'ART' : 'Artifact',
        'EMT' : 'Enchantment',
        'PLW' : 'Planeswalker',
        'INT' : 'Instant',
        'SOR' : 'Sorcery',
        'LAN' : 'Land'
  }

# --- DEFINING GLOBAL FUNCTIONS ---

def populateDeckList(decklist):
    
    # list comprehension returns card objects based on decklist contents
    
    return tuple([(Card.objects.get(id=card.card_id), card.quantity) for card in decklist])

def cardTypeFilter(cardTypes, cardInfo):
    
    return filter(lambda card: any(card[0].card_type.startswith(cardType) for cardType in cardTypes), cardInfo)

def findSetName(cardObject):
    
    # converts set ID associated with card to common translator for set name, following DNRY table design 
    return ExpansionSet.objects.filter(id = cardObject.expansion_set_id).values_list('expansion_name', flat=True).get()

def AUDtoUSD(value):
    
    """
        Rate  set by  mgmt command "fx retriever", updates FX on schedule
    """
        
    value *= decimal.Decimal(Forex.objects.filter(pair__exact="USD/AUD").first().rate)
    
    return value

def getCardImage(card_id):
    
    card = get_object_or_404(Card, id = card_id)
    
    """
    url = "https://api.scryfall.com/cards/"+card.expansion_set_id+"/"+number+"/"
    image request = https://api.scryfall.com/cards/xln/234?format=image
    back image request = https://api.scryfall.com/cards/xln/234?format=image&face=back

    """
    
    card_set = str(card.expansion_set).strip().lower()
    number = str(card.collector_number)
    url = "https://api.scryfall.com/cards/"+card_set+"/"+number+"/"
    
    try:
        req = requests.get(url)
        req.raise_for_status()
        payload = json.loads(req.text)
        if "card_faces" in payload :
            card.image = payload["card_faces"]["0"]["image_uris"]["normal"]
            card.back = payload["card_faces"]["1"]["image_uris"]["normal"]
        else:
            card.image = payload["image_uris"]["normal"]
            card.back = None
    except requests.exceptions.HTTPError as e:
        card.image = e.response.text
    
    return card.image, card.back

# --- VIEWS ---

def index(request):
    latestDecks = Deck.objects.order_by('id')[:5]
    
    for deck in latestDecks:
        deck.decklist = Decklist.objects.filter(deck_id = deck.id)
        
        cardInfo = populateDeckList(deck.decklist)
        
        deck.deckValue = 0
        
        for card, quantity in cardInfo:
            # card image, card back should be grabbed by javascript as its a hover effect
            # how to do this?
            # iframe preview to card view
            # use javascript to set card-preview to active / inactive
            # iframe is filled with appropriate preview on link hover
            card.expansion_set_id = findSetName(card)
            card.current_price = AUDtoUSD(card.current_price)
            card.totalValue = card.current_price * quantity
            deck.deckValue += card.totalValue
            
        deck.creatureList = cardTypeFilter(['CTR'], cardInfo)
        deck.creatureListQuantity = sum(quantity for _, quantity in cardTypeFilter(['CTR'], cardInfo))
        
        deck.planeswalkerList = cardTypeFilter(['PLW'], cardInfo)
        deck.planeswalkerListQuantity = sum(quantity for _, quantity in cardTypeFilter(['PLW'], cardInfo)) 
        
        deck.landList = cardTypeFilter(['LAN'], cardInfo)
        deck.landListQuantity = sum(quantity for _, quantity in cardTypeFilter(['LAN'], cardInfo))
        
        deck.spellList = cardTypeFilter(['INT', 'SOR'], cardInfo)
        deck.spellListQuantity = sum(quantity for _, quantity in cardTypeFilter(['INT', 'SOR'], cardInfo))        
        
        deck.deckFormat = MTG_FORMATS[deck.deck_format]
    
    context = {
            'latestDeckList' : latestDecks
            }
    
    return render(request, 'mtgdatabase/index.html', context)

def card(request, card_id):
    
    """
    Objective is to provide an overview of a given card
    TO-DO:
        * Grab image of card from scryfall to display [DONE 13/02/2021]
        * Value of the card
        * Decks card is a part of and their format
        * Copies owned
        * Copies in decks in db total
    """
    
    #card.expansion_set_id = findSetName(card)
    
    card = get_object_or_404(Card, id = card_id)
    
    card.image, card.back = getCardImage(card_id)
    
    context = {
            'card' : card
            }
    
    return render(request, 'mtgdatabase/card.html', context)

def deck(request, deck_id):
    
    """
    Objective is to provide statistics, in-depth analysis vs index summary
    TO-DO:
        * Indicate Resale Values [DONE 02/02/2021]
        * Indicate how many copies owned for a particular card
        * Work out how many copies used (deck = constructed, present in constructed decklist)
        * $ to complete deck build
        
    """
    
    # grab deck object out of db
    deckObject = get_object_or_404(Deck, id = deck_id)
    
    # find the cards in the deck
    decklist = Decklist.objects.filter(deck_id = deck_id)
    
    # grab the (card object, decklist quantity) information
    cardInfo = populateDeckList(decklist)
    
    deckValue = 0
    resaleValue = 0
    
    # manipulate card object for display
    for card, quantity in cardInfo:
        card.expansion_set_id = findSetName(card)
        card.current_price = AUDtoUSD(card.current_price)
        card.totalValue = card.current_price * quantity
        deckValue += card.totalValue
        if card.current_price > 5:
            resaleValue += card.totalValue
        
    # sort out what goes where for deck front end display
    # for quantity values
    # -- repeat function call or filter in memory is discarded
    
    # can this be done by accessing something in the db rather than hardcoding?
    # iterating through a model or table would be less code potentially?
    # keep an eye out for possible alternative solution
    creatureList = cardTypeFilter(['CTR'], cardInfo)
    creatureListQuantity = sum(quantity for _, quantity in cardTypeFilter(['CTR'], cardInfo))
    
    planeswalkerList = cardTypeFilter(['PLW'], cardInfo)
    planeswalkerListQuantity = sum(quantity for _, quantity in cardTypeFilter(['PLW'], cardInfo)) 
    
    landList = cardTypeFilter(['LAN'], cardInfo)
    landListQuantity = sum(quantity for _, quantity in cardTypeFilter(['LAN'], cardInfo))
    
    spellList = cardTypeFilter(['INT', 'SOR'], cardInfo)
    spellListQuantity = sum(quantity for _, quantity in cardTypeFilter(['INT', 'SOR'], cardInfo))
    
    # get the value for the field, Flat=true means it is not a Query Set result        
    # below are what we needed when deckObject was incorrectly a filter instead of a get
    #deckName = deckObject.values_list('deck_name', flat=True).get()
    #deckFormat = MTG_FORMATS[deckObject.values_list('deck_format', flat=True).get()]
    
    deckFormat = MTG_FORMATS[deckObject.deck_format]
        
    context = {
            'deck': deckObject,
            'deckFormat': deckFormat,
            'deckValue' : deckValue,
            'resaleValue': resaleValue,
            'creatureList' : creatureList,
            'creatureListQuantity' : creatureListQuantity,
            'planeswalkerList' : planeswalkerList,
            'planeswalkerListQuantity' : planeswalkerListQuantity,
            'landList' : landList,
            'landListQuantity' : landListQuantity,
            'spellList' : spellList,
            'spellListQuantity' : spellListQuantity
            }
        
    return render(request, 'mtgdatabase/deck.html', context)

def wishlist(request, wishlist_id):
    return HttpResponse("This page will show a card someone has added to a wishlist. This is the current wishlist: %s." % wishlist_id)

def constructed_deck(request, deck_id, decklist_id):
    return HttpResponse("This page will show links to all decks that have been created")

def wishlist_deck(request, wishlist_id):
    return HttpResponse("This page will show links to all decks that are not built")

def edit_card(request, card_id):
    return HttpResponse("This page will allow new cards to be added to wishlist or collection")