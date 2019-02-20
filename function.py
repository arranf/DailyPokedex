import datetime
import csv
import random
import os
import json

import requests
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import *

# .env file import - comment out for deployment
from dotenv import load_dotenv
load_dotenv()

LEGENDARY_IDS = [144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649 ]
BASE = 'https://pokeapi.co/api/v2/'

def get_pokemon_data(id):
    r = requests.get(BASE + 'pokemon/' + id)
    return r.json()

def get_species(id):
    r = requests.get(BASE + 'pokemon-species/' + id)
    return r.json()

def get_pokemon_id():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        with open('pokedex.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == today:
                    return row[0]
    except:
        print('Error opening pokedex.csv')

def send_sms(text):
    # Your Account SID from twilio.com/console
    account_sid = os.getenv("TWILIO_SID")
    # Your Auth Token from twilio.com/console
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=os.getenv("TO_NUMBER"), 
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        body=text)

def send_email(text, image_url):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("pokedex@arranfrance.com")
    to_email = Email(os.environ.get('TO_EMAIL'))
    today_long = datetime.datetime.today().strftime('%A %d %B %Y')
    subject = f"Your Daily Pokemon for {today_long}"
    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    mail.add_content(Content("text/html", f"<img src=\"{image_url}\"\> <br>" + text))
    sg.client.mail.send.post(request_body=mail.get())
    
def get_text(pokemon, id):
    if pokemon is None:
        #TODO ERROR
        pass
    species = get_species(pokemon['species']['name'])

    types = ''
    type_count = len(pokemon['types'])
    for i, t in enumerate(pokemon['types']):
        types = types + t['type']['name'] 
        if type_count > 1 and i < type_count - 1:
            types = types + (', ' if i < len(pokemon['types']) - 2 else ', and ' )

    name = (next(x for x in species['names'] if x['language']['name'] == 'en'))['name']
    flavor_texts = (x for x in species['flavor_text_entries'] if x['language']['name'] == 'en')
    flavor_text = random.choice(list(flavor_texts))['flavor_text'].replace('\n',' ').replace('\t', ' ')
    height = pokemon['height'] * 0.1
    weight = pokemon['weight'] * 0.1
    is_legendary = ' legendary ' if int(id) in LEGENDARY_IDS else '' 
    color = species['color']['name']
    genus = (next(x for x in species['genera'] if x['language']['name'] == 'en'))['genus']

    text = f'Master Hawksley! Today\'s Pokémon is {name}, the {genus}. {name} is a {color} {types}{is_legendary} Pokemon which stands {height:.2g}m tall and weighs {weight:.2g}kg. {flavor_text}'
    text = ' '.join(text.split()) # single space it all
    return text

def send():
    id = get_pokemon_id()
    print(f'Id is {id}')
    pokemon = get_pokemon_data(id)
    name = pokemon['name']
    print(f'Pokemon is {name}')
    text = get_text(pokemon, id)
    print(text)
    sprite_url = pokemon['sprites']['front_default'] if random.random() < 0.9 else pokemon['sprites']['front_shiny']
    send_email(text, sprite_url)
    send_sms(text)