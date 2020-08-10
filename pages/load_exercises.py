# this script loads all exercises to the exercise database from "exercises.txt"
import sys
import os
import django

sys.path.append('/Users/umut/Desktop/DjangoProjects/KivancWannabes')
os.environ['DJANGO_SETTINGS_MODULE'] = 'KivancWannabes.settings'
django.setup()

from pages.models import Exercise

file_path = 'exercises.txt'

try:
    exercises_txt = open(file_path, 'r')
    # iterate over exercises.txt line by line.
    for line in exercises_txt:
        exercise_name = line.split(',')[0]
        # if the exercise exist in the database then pass.
        if Exercise.objects.filter(name=exercise_name):
            pass
        # if the exercise does not exist in the database then create and save that exercise to the database.
        else:
            # temporary exercise to save database.
            temp_exercise = Exercise(name=exercise_name)
            temp_exercise.save()


except FileNotFoundError:
    print('exercises.txt could not find')
