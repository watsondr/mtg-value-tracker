# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:09:59 2020

@author: campb

The purpose of this file is to retrieve data to add in to the database

To use this file call python manage.py data_retriever from MTGDeckValueTracker folder in command line

# TO DO: Where are we grabbing data from? scryfall API? [DONE 23/06/2020]
# TO DO: Drop all test data in card table [DONE 02/07/2020]
# TO DO: Change model to accept a 3 letter code based on format [DONE 02/07/2020]
# TO DO: Extend model to have a set collector number to meet dataa source needs [DONE 02/07/2020]
# TO DO: Use model fields to dynamically call API [DONE 03/07/2020 ... 12.26am]

# TO DO: create loop through db and iterate through cards [DONE 22/07/2020]
# TO DO: update latest price field [DONE 22/07/2020]
# TO DO: update movement price column [DONE 30/07/2020]

# TO DO: Make progress bar for cmd line [DONE 02/02/2021]
"""

from django.core.management.base import BaseCommand, CommandError
from mtgdatabase.models import Card
from decimal import Decimal
from datetime import datetime
import json, requests
import time

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        #url = "https://api.scryfall.com/cards/named?exact=narcomoeba"
        #url = "https://api.scryfall.com/cards/multiverse/452797"
        #url = "https://api.scryfall.com/cards/grn/47"
        
        
        """
        ===============================================================
        START DB SETTERS
        ===============================================================
        """
        
        def update_latest_price(price, card):
            card.current_price = Decimal(price)
            card.save()
            
        def update_movement_price(price, card):
            originalPrice = card.original_price
            currentPrice = card.current_price
            priceMove = ((currentPrice - originalPrice) / originalPrice) * 100
            card.movement_price = float(round(priceMove,3))
            card.save()
            
        def confirm_historical_high(price, card):
            currentPrice = card.current_price
            historicalHigh = card.historical_high
            
            if currentPrice > historicalHigh:
                card.historical_high = currentPrice
                card.historical_high_date = datetime.today().strftime("%Y-%m-%d")
                card.save()
            
        """
        ===============================================================
        END DB SETTERS
        ===============================================================
        """
        
        """
        ===============================================================
        START PROGRESS BAR
        ===============================================================
        """
        
        # Print iterations progress
        def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
            """
            Call in a loop to create terminal progress bar
            @params:
                iteration   - Required  : current iteration (Int)
                total       - Required  : total iterations (Int)
                prefix      - Optional  : prefix string (Str)
                suffix      - Optional  : suffix string (Str)
                decimals    - Optional  : positive number of decimals in percent complete (Int)
                length      - Optional  : character length of bar (Int)
                fill        - Optional  : bar fill character (Str)
                printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
            """
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
            # Print New Line on Complete
            if iteration == total: 
                print()
        """
        ===============================================================
        END PROGRESS BAR
        ===============================================================
        """

        starttime = time.time()
        cards = Card.objects.all()
        card_count = Card.objects.count()
        
        print("Card objects loaded. Starting database update. Please wait.")
        printProgressBar(0, card_count, prefix='Cards Loading:', suffix='Complete', length=50)
        
        for i, card in enumerate(cards):
            card_set = str(card.expansion_set).strip().lower()
            number = str(card.collector_number)
            url = "https://api.scryfall.com/cards/"+card_set+"/"+number+"/"
            
            try:
                req = requests.get(url)
                req.raise_for_status()
                payload = json.loads(req.text)
                price = payload["prices"]["usd"]
            except requests.exceptions.HTTPError as e:
                print(e.response.text)
                price = 0
            
            # now update card row in db
            update_latest_price(price, card)
            update_movement_price(price, card)
            confirm_historical_high(price, card)
            
            time.sleep(0.25 - ((time.time() - starttime) % 0.25))
            
            # update progress bar
            printProgressBar(i + 1, card_count, prefix='Cards Loading:', suffix='Complete', length=50)
            
        print("Database update complete.")