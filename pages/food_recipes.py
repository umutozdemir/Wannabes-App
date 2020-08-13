# this script find youtube links of food recipes with searching food names on youtube.
import sys
import os
import django
import requests

sys.path.append('/Users/umut/Desktop/DjangoProjects/KivancWannabes')
os.environ['DJANGO_SETTINGS_MODULE'] = 'KivancWannabes.settings'
django.setup()

from pages.models import Food

foods = Food.objects.all()
search_url = 'https://www.googleapis.com/youtube/v3/search'
for food in Food.objects.all():
    try:
        search_string = 'how to make ' + food.name
        params = {
            'part': 'snippet',
            'q': search_string,
            'key': 'AIzaSyDvGA_Vh18Vk3AKVep0NAkOYmiZcNLJKDo',
            'maxResults': 1
        }
        r = requests.get(search_url, params=params).json()
        recipe_link = 'youtube.com/watch?v=' + r['items'][0]['id']['videoId']
        food.recipe_link = recipe_link
        food.save()
    except (IndexError, KeyError):
        print(search_string)

#97.ci food objesinde durdu.