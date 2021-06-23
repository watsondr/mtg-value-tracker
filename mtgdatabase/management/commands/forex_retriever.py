# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 23:22:21 2020

@author: campb

The purpose of this file is to retrieve and set Forex rates.
Right now the only rate in the model is USD/AUD

TO DO: Make progress bar for cmd line IF forex retrieval becomes more complex
"""

from django.core.management.base import BaseCommand, CommandError
from mtgdatabase.models import Forex
from datetime import datetime
import requests, json

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        """
        ===============================================================
        START DB SETTERS
        ===============================================================
        """
        
        def update_latest_rate(price, forex):
            forex.rate = price
            forex.edit_time = datetime.today().strftime("%Y-%m-%d")
            forex.save()
        
        """
        ===============================================================
        END DB SETTERS
        ===============================================================
        """
        
        fxPair = Forex.objects.filter(pair__exact="USD/AUD").first()
        
        url = "https://api.exchangeratesapi.io/latest?base=USD&symbols=USD,AUD"
        
        try:
            req = requests.get(url)
            req.raise_for_status()
            payload = json.loads(req.text)
            price = payload["rates"]["AUD"]
        except requests.exceptions.HTTPError as e:
            print(e.response.text)
            price = 1
        
        update_latest_rate(price, fxPair)
        
        print("Forex price update complete.")