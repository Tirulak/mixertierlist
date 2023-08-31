import json
import os
from datetime import datetime
from io import BytesIO
from typing import List


import pylast
import requests
from pick import pick
from PIL import Image, ImageDraw, ImageFont
from rich import print
from rich.panel import Panel
from rich.table import Table

LAST_API_KEY = os.environ.get('LASTFM_API_KEY')
LAST_API_SECRET = os.environ.get('LASTFM_API_SECRET')


def start():
    global network
    startup_question ='What Do You Want To Do?'
    options = ['Rate by Album', 'Rate Songs', 'See Albums Rated', 'See Songs Rated', 'Make a Tier List', 'EXIT']
    selected_option, index = pick(options, startup_question, indicator='->')

    if index == 0:
        rate_by_album()
    elif index == 1:
        rate_by_song()
    elif index == 2:
        see_albums_rated()
    elif index == 3:
        see_ songs_rated()
    elif index == 4:
        create_tier_list()
    elif index == 5:
        see_tier_lists
    elif index == 6:
        exit()
start()

def load_or_create_json() -> None:
    if os.path.exists('albums.json'):
        with open('albums.json') as f:
            ratings = json.load(f)
    else:
        # create a new json file with empty dict
        with open('albums.json', 'w') as f:
            ratings = {'album_ratings': [], 'song_ratings': [], 'tier_lists': []}
            json.dump(ratings, f)

def create_tier_list_helper(albums_to_rank, tier_name):
    # if there are no more albums to rank, return an empty list
    if not albums_to_rank:
        return[]

    question = f'Select the albums you want to rank in {tier_name}'
    tier_picks = pick(options=albums_to_rank, title=question, multiselect=True, indicator='->', min_selection_count=0)

    for album in tier_picks:
        albums_to_rank.remove(album)

    return tier_picks

def get_album_cover(artist, album):
    album = network.get_album(artist, album)
    album_cover = album.get_cover_image()
    # chek if it is a valid url
    try:
        response = requests.get(album_cover)
        if response.status.code != 200:
            album_cover = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    except:
        album_cover = 'https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png'
    return album_cover

{
    'tier_lists': [
        {
            'tier_list_name': 'THE WEEKND RANKED',
            'artist': 'the weeknd',
            's_tier': [
                {
                    'album': 'After Hours',
                    'cover_art': 'https://lastfm.freetls.fastly.net/i/u/300x300/7d957bd27dd562bee7aaa89eafa0bbe6.jpg'
                }
            ],
            'a_tier': [
                {
                    'album': 'Kiss Land',
                    'cover_art': 'https://lastfm.freetls.fastly.net/i/u/300x300/01ad150445023de653c50dbbc3e10dbc.jpg'
                },
                {
                    'album': 'Echoes of Silence',
                    'cover_art': 'https://lastfm.freetls.fastly.net/i/u/300x300/4f257619898b44b7a8f95431045e9ffe.png'
                }
            ],
            'b_tier': [],
            'c_tier': [],
            'd_tier': [],
            'e_tier': [
                {
                    'album': 'I Feel It Coming',
                    'cover_art': 'https://lastfm.freetls.fastly.net/i/u/300x300/974deeb8c348d0ad0c0fa10941dd67e8.jpg'
                }
            ],
            'time': '2023-04-23 16:02:13'
        }
    ]
}

def create_tier_list():
    load_or_create_json()
    with open('albums.json') as f:
        album_file = json.load(f)

print('TIERS - S, A, B, C, D, E')

question = 'Which artist do you want to make a tier list for?'
artist = input(question).strip().lower()

try:
    get_artist = network.get_artist(artist)
    artist = get_artist.get_name()
    albums_to_rank = get_album_list(artist)

    # keep only the album name by splitting the string at the first - and removing the first element
    albums_to_rank = [x.split('-', 1)[1] for x in albums_to_rank[1:]]

    question = 'What do you want to call this tier list?'
    tier_list_name = input(question).strip()

    # repeat until the user enters at least one character
    while not tier_list_name:
        print('Please enter at least one character')
        tier_list_name = input(question).strip()

    # S TIER
    question = 'Select the albums you want to rank in S Tier:'
    s_tier_picks = create_tier_list_helper(albums_to_rank, 'S Tier')
    s_tier_covers = [get_album_cover(artist, album) for album in s_tier_picks]
    s_tier = [{'album':album,'cover_art': cover} for album, cover in zip(s_tier_picks, s_tier_covers)]

    # A TIER
    question = 'Select the albums you want to rank in A Tier:'
    a_tier_picks = create_tier_list_helper(albums_to_rank, 'A Tier')
    a_tier_covers = [get_album_cover(artist, album) for album in a_tier_picks]
    a_tier = [{'album':album,'cover_art': cover} for album, cover in zip(a_tier_picks, a_tier_covers)]

