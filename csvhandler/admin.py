from django.contrib import admin

# Register your models here.
from .models import CardImport, DeckImport

admin.site.register(CardImport)
admin.site.register(DeckImport)