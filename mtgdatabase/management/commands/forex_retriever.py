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
        
        with open("mtgdatabase\static\mtgdatabase\json\credentials.json", "r") as read_file:
            credentials_data = json.load(read_file)
            
        KEY = credentials_data["currency-converter"]["x-rapidapi-key"]
        HOST = credentials_data["currency-converter"]["x-rapidapi-host"] 
        
        url = "https://currency-converter5.p.rapidapi.com/currency/convert"
        
        querystring = {"format":"json","from":"USD","to":"AUD","amount":"1"}
        
        headers = {
            'x-rapidapi-key': KEY,
            'x-rapidapi-host': HOST
            }
        
        try:
            req = requests.get(url, headers=headers, params=querystring)
            req.raise_for_status()
            payload = json.loads(req.text)
            price = payload["rates"]["AUD"]["rate"]
        except requests.exceptions.HTTPError as e:
            print(e.response.text)
            """
            No longer set price here as it impedes debugging,
            if vendor service has a policy change.
            """
        
        fxPair = Forex.objects.filter(pair__exact="USD/AUD").first()
        
        update_latest_rate(price, fxPair)
        
        print("Forex price update complete.")