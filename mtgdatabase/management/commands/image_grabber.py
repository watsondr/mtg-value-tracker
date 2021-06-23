# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:58:58 2021

@author: campb

Purpose of this script is to fill the db with images by placing them in the right folder.

Should follow these steps:
    * See what the card image location value is for the card. [DONE 10/4/21]
    * IF it is default (mtgdatabasessets\card-front\default.jpg OR default.jpg): do something, otherwise, do nothing [10/4/21]
    * when doing something:
        * go to scryfall and grab an image [10/4/21S]
        * save the image in to D:\Programs\Dropbox\Cross Computer Coding\Python Projects\MTGDeckValueTracker\mtgdatabase\static\mtgdatabase\assets\card-front
        * update card's image_id field with this syntax: <Card.id>.jpg
    
"""

from django.core.management.base import BaseCommand, CommandError
from mtgdatabase.models import Card
from pathlib import Path
from PIL import Image
import time, requests, json, re

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        starttime = time.time()
        cards = Card.objects.all()
        id_regex = re.comiple('[\d+]\.jpe?g')
        file_location = Path(r'D:\Programs\Dropbox\Cross Computer Coding\Python Projects\MTGDeckValueTracker\mtgdatabase\static\mtgdatabase\assets\card-front')
        
        """
        test_url = 
        """
        
        
        
        """
        
        for i, card in enumerate(cards):
            
            """
            """
            CHECK THE CARD IMAGE LOCATION AND PROCEED FROM THERE
            
            Core Concept: Do no API calls where card image exists
            """
            """
            
            if card.image_id != id_regex:
            
                card_set = str(card.expansion_set).strip().lower()
                number = str(card.collector_number)
                url = "https://api.scryfall.com/cards/"+card_set+"/"+number+"/"
                
                try:
                    req = requests.get(url)
                    req.raise_for_status()
                    payload = json.loads(req.text)
                    if "card_faces" in payload :
                        card.image = payload["card_faces"]["0"]["image_uris"]["normal"]
                    else:
                        card.image = payload["image_uris"]["normal"]
                except requests.exceptions.HTTPError as e:
                    card.image = e.response.text
                    
                """
                """
                OPEN FOLDER LOCATION
                """
                
                
                    
                """
                SAVE IMAGE TO FILE
                """
                """
                
                
                time.sleep(0.25 - ((time.time() - starttime) % 0.25))
                
        """