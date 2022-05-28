import csv, io
from django.shortcuts import render
from django.contrib import messages
from mtgdatabase.models import Card, Deck

# Create your views here
# new views should be registered in mtgdatabase/urls.py

"""
Accessed 21st June 2020: https://medium.com/@simathapa111/how-to-upload-a-csv-file-in-django-3a0d6295f624

This function is to help as a postgreSQL database update tool using data sourced via a provided .csv file for the mtgdatabase app

To-do: Make it a universal tool that maps fields from any csv to any db for django

SEE INSIDE FOR LOOP WITH CARD READER, IT SETS WHICH TABLE THE UPLOADER IS ADDING DATA TOWARDS

LET THE USER SET A VARIABLE TO CHANGE THE TABLE!!

NOTE 04/11/2020: This can be done with class based views potentially. Based on the class model being passed in,
the algorithm tree will change.

Need a model for each mtgdatabase in models.py for csvhandler

"""

def cardimport_upload(request):
    
    template = "csvhandler/cardImport_upload.html"
    data = Card.objects.all()
    
    prompt = {
            'order': 'Order of the CSV should be name, type, rarity, collector number, set, price and amount owned.',
            'cards': data
            }
    
    if request.method == "GET":
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']
    
    # validate that it is a CSV file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'The file was not recognised by the importer as a CSV file.')

    data_set = csv_file.read().decode('cp1252')
    
    # a stream iterates through the file contents
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):

        """
        if csv is using code names
        expansion = ExpansionSet.objects.get(code=column[3])
        then use expansion_set = expansion
        """
    
        # this line discards the update, keeps the create
        _, created = Card.objects.update_or_create(
                    card_name=column[0],
                    card_type=column[1],
                    rarity=column[2],
                    expansion_set_id=column[3],
                    collector_number=column[4],                    
                    original_price=column[5],
                    quantity_owned=column[6],
                    movement_price=column[7],
                    current_price=column[8],
                    historical_high=column[9]
        )
    context = {}
    return render(request, template, context)
    
    """
    template = "cardImport_upload.html"
    data = ExpansionSet.objects.all()
    
    prompt = {
            'order': 'Order of the CSV should be name, type, rarity, set, price and amount owned.',
            'cards': data
            }
    
    if request.method == "GET":
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']
    
    # validate that it is a CSV file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'The file was not recognised by the importer as a CSV file.')
        
    data_set = csv_file.read().decode('UTF-8')
    
    # a stream iterates through the file contents
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        # this line discards the update, keeps the create
        _, created = ExpansionSet.objects.update_or_create(
                    expansion_name=column[0],
                    code=column[1]
        )
    context = {}
    return render(request, template, context)

    """
    
    """
    Parameters
    ----------
    request : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
def deckImport_upload(request):
    data = Deck.objects.all()
    template = data # change this
    context = {}
    return render(request, template, context)
    
def genericImport(request, importType, data):
    """
    The idea of this view is that by receiving an importType and data,
    we can route the uplaod request to the correct view to implement into db
    
    these are links of interest (04/09/2021):
        https://stackoverflow.com/posts/59369795/revisions
        https://docs.djangoproject.com/en/3.0/ref/class-based-views/base/#django.views.generic.base.TemplateView
    
    by making a template view we may need to establish a class
    and then treat the class as a view.
    
    Codewise - looks cleaner
    """