# this script deletes duplicates of some database objects.
import sys
import os
import django

sys.path.append('/Users/umut/Desktop/DjangoProjects/KivancWannabes')
os.environ['DJANGO_SETTINGS_MODULE'] = 'KivancWannabes.settings'
django.setup()
from pages.models import Exercise

exercises = Exercise.objects.all()
exercise_names = [exercise.name for exercise in exercises]
for exercise_name in exercise_names:
    try:
        exercise = Exercise.objects.get(name=exercise_name)
    except Exercise.MultipleObjectsReturned:
        exercise_to_delete = Exercise.objects.filter(name=exercise_name)[1]
        exercise_to_delete.delete()
