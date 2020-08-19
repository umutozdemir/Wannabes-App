# this script find youtube search links of foods and exercises with searching food and exercise names on youtube.
import sys
import os
import django
from django.db import DataError

sys.path.append('/Users/umut/Desktop/DjangoProjects/KivancWannabes')
os.environ['DJANGO_SETTINGS_MODULE'] = 'KivancWannabes.settings'
django.setup()

from pages.models import Food, Exercise

food_set = Food.objects.all()

for food in food_set:
    try:
        food_search_string = 'https://www.youtube.com/results?search_query='
        search_query = 'how to make ' + food.name
        food_search_string += search_query
        food.recipe_link = food_search_string
        food.save()
    # when a video link is too long django raise a DataError exception.
    except DataError:
        food.recipe_link = 'https://www.youtube.com'
        food.save()


exercise_set = Exercise.objects.all()

for exercise in exercise_set:
    try:
        exercise_search_string = 'https://www.youtube.com/results?search_query='
        search_query = 'how to ' + exercise.name
        exercise_search_string += search_query
        exercise.video_link = exercise_search_string
        exercise.save()
    # when a video link is too long django raise a DataError exception.
    except DataError:
        exercise.video_link = 'https://www.youtube.com'
        exercise.save()
