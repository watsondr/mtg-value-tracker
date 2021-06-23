from django.db import models
from django.core.validators import MinValueValidator

# SEE MTG.XLSX for design document and intention inspiration

"""
This is the table setup if you want to expand and introduce accounts.

There are very few new fields but any current databases will have to have
data moved around.

TABLE customer
- id
- member_number
- password

-customer_card
- id
- card_id (FK)
- original_price
- movement_price
- historical_high
- historical_high_date
- quantity_owned

card
- id
- rarity
- set
- collector_number
- current_price

wishlist
- id
- card
- quanity
- member_number
- watchlist_name

TO DO : Add in expansion set to decklist for clarity of which card it is
TO DO : Decklist return to add expansionSet __str__(self) 
"""

    
class ExpansionSet(models.Model):
    
    expansion_name = models.CharField(max_length = 75)
    code = models.CharField(max_length = 4)
    
    def __str__(self):
        return self.code

class Deck(models.Model):
    
    # Many to Many Relationship with Card
    
    # Choices definition
    COMMANDER = 'COM'
    VINTAGE = 'VNT'
    LEGACY = 'LEG'
    MODERN = 'MOD'
    PIONEER = 'PIO'
    STANDARD = 'STD'
    PAUPER = 'PAU'
    MTG_FORMATS = [
            (COMMANDER, 'Commander'),
            (VINTAGE, 'Vintage'),
            (LEGACY, 'Legacy'),
            (MODERN, 'Modern'),
            (PIONEER, 'Pioneer'),
            (STANDARD, 'Standard'),
            (PAUPER, 'Pauper'),
    ]
    
    deck_name = models.CharField(max_length=50, verbose_name = 'Deck Name')
    deck_format = models.CharField(
            max_length = 3,
            choices = MTG_FORMATS,
            default = COMMANDER,
            verbose_name = 'Format',
    )
    constructed = models.BooleanField(default = False)
    
    def __str__(self):
        return self.deck_name
    

class Card(models.Model):
    
    # Choices definition 
    
    # CARDS 
    # Interrupts should be mapped to instant
    
    CREATURE = 'CTR'
    ARTIFACT = 'ART'
    ENCHANTMENT = 'EMT'
    PLANESWALKER = 'PLW'
    INSTANT = 'INT'
    SORCERY = 'SOR'
    LAND = 'LAN'
    CARD_TYPES = [
            (CREATURE, 'Creature'),
            (ARTIFACT, 'Artifact'),
            (ENCHANTMENT, 'Enchantment'),
            (PLANESWALKER, 'Planeswalker'),
            (INSTANT, 'Instant'),
            (SORCERY, 'Sorcery'),
            (LAND, 'Land'),
    ]
    
    # RARITIES
    COMMON = 'COM'
    UNCOMMON = 'UCO'
    RARE = 'RAR'
    MYTHIC = 'MYC'
    RARITIES = [
            (COMMON, 'Common'),
            (UNCOMMON, 'Uncommon'), 
            (RARE, 'Rare'),
            (MYTHIC, 'Mythic'),
    ]
    
    card_name = models.CharField(max_length=200, verbose_name= 'Name')
    card_type = models.CharField(
               max_length = 3,
               choices = CARD_TYPES,
               default = CREATURE,
               verbose_name = 'Card Type'
    )
    rarity = models.CharField(
            max_length = 3,
            choices = RARITIES,
            default = COMMON,
            verbose_name = 'Rarity'
    )
    
    expansion_set = models.ForeignKey(ExpansionSet, on_delete = models.CASCADE)
    collector_number = models.IntegerField(default = 0)
    original_price = models.DecimalField(max_digits = 10, decimal_places = 2, editable = False)
    movement_price = models.FloatField(editable = False)
    current_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    historical_high = models.DecimalField(max_digits = 10, decimal_places = 2)
    historical_high_date = models.DateField('Highest Value Date', auto_now_add = True)
    quantity_owned = models.IntegerField(validators=[MinValueValidator(0, 'Quantity owned must be greater or equal to 0')])
    image_id = models.CharField(max_length = 50, default = 'mtgdatabase\assets\card-front\default.jpg', verbose_name = 'Image ID') # Same for front and back folders
    
    def __str__(self):
        return self.card_name
    
class Wishlist(models.Model):
    
    # Capcity for 1 wishlist per user 
    
    card = models.ForeignKey(Card, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    def __str__(self):
        return str(self.card)
    
    
class Decklist(models.Model):
    
    # Documentation Source:
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#manytomanyfield
    # ManyToManyField.through_fields
    
    # does quantity need to be a seperate table with card foreign key as primary key?
    
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1, 'Quantity in Deck must be greater than 1')])
    edit_time = models.DateTimeField('Last edited', auto_now = True)
    
    def __str__(self):
        return str(self.deck) + " // " + str(self.card) + " // " + str(self.card.collector_number)
    
class Forex(models.Model):
    
    pair = models.CharField(max_length=50, verbose_name = 'Forex Pair')
    rate = models.DecimalField("FX Rate", max_digits = 8, decimal_places = 7)
    edit_time = models.DateTimeField('Last edited', auto_now = True)
    
    def __str__(self):
        return self.pair