from django.db import models

# Create your models here.

class CardImport(models.Model):
    name_import = models.CharField(max_length = 200)
    type_import = models.CharField(max_length = 3)
    rarity_import = models.CharField(max_length = 3)
    set_import = models.CharField(max_length=75)
    price_import = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity_import = models.IntegerField()
    
    def __str__(self):
        return self.name
    
#class ExpansionSetImport(modesl.Model):

class DeckImport(models.Model):
    deck_name_import = models.CharField(max_length=50)
    deck_format_import = models.CharField(max_length = 3)
    constructed_import = models.BooleanField(default = False)