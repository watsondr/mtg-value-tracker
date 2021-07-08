# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:58:58 2021

@author: campb

Purpose of this script is to fill the db with images by placing them in the right folder.

Should follow these steps:
    * See what the card image location value is for the card. [DONE 10/4/21]
    * IF it is default (mtgdatabasessets\card-front\default.jpg OR default.jpg): do something, otherwise, do nothing [10/4/21]
    * when doing something:
        * go to scryfall and grab an image [10/4/21]
        * save the image in the approrpriate folder (variable established) [26/6/21]
        * update card's image_id field with this syntax: <Card.id>.jpg [26/6/21]
        
    https://stackoverflow.com/questions/50948061/how-to-save-or-download-an-image-that-i-get-in-a-request-python
    https://stackoverflow.com/questions/55147650/how-do-i-download-images-using-the-scryfall-api-and-python
    
    * What is the best way to store images in a db & should we be doing that instead?
    
    * Optimise so that cards already with imagary are skipped and loop progresses to next row
    
    * Implement progress bar
    
"""

from django.core.management.base import BaseCommand
from mtgdatabase.models import Card
from pathlib import Path
import time, requests, re, os

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        starttime = time.time()
        cards = Card.objects.all()
        id_regex = re.compile('[\d+]\.jpe?g') 
        file_location = Path(r'D:\Coding\mtg-value-tracker\mtg-value-tracker\mtgdatabase\static\mtgdatabase\assets\card-front')
        
        # THIS IS CORRECT WAY TO DECLARE FILE LOCATION
        #file_location = os.path.join(file_location, '40.jpg')
        
        for i, card in enumerate(cards):
            
            """
            CHECK THE CARD IMAGE LOCATION AND PROCEED FROM THERE
            
            Core Concept: Do no API calls where card image exists
            """

            def image_function(payload, size):
                """
                This function condensces lines of code in case of expansion to front and back of cards
                """

                image_uris = payload
                image = requests.get(image_uris[size])
                image.raise_for_status()
                with open(os.path.join(file_location, str(card.id) + '.jpg'), 'wb') as file:
                    file.write(image.content)
            
            # checking the jpg is not default
            if card.image_id != id_regex:
                card_set = str(card.expansion_set).strip().lower()
                number = str(card.collector_number)
                url = "https://api.scryfall.com/cards/"+card_set+"/"+number+"/"

                try:
                    req = requests.get(url)
                    req.raise_for_status()
                    payload = req.json()
                    image_function(payload['image_uris'], 'normal')
                        
                    card.image_id = str(card.id) + '.jpg'
                    card.save()
                except requests.exceptions.HTTPError as e:
                    card.image = e.response.text        
                 
            time.sleep(0.25 - ((time.time() - starttime) % 0.25))