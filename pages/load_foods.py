# this script loads all foods with its calories from 'food_data.xlsx'
import sys
import os
import django

sys.path.append('/Users/umut/Desktop/DjangoProjects/KivancWannabes')
os.environ['DJANGO_SETTINGS_MODULE'] = 'KivancWannabes.settings'
django.setup()

from pages.models import Food

file_path = 'food_data.csv'

try:
    food_data_csv = open(file_path, 'r')
    # iterate over food_data.csv line by line.
    for line in food_data_csv:
        food_data = line.split(';')
        # food_data is an array that split the line with ';'
        # food_data[0] -> id of the food.
        # food_data[1] -> name of the food.
        # food_data[2] -> food group.
        # food_data[3] -> calorie of food in 100 gr.
        # food_data[4] -> amount of fat(gr) in 100 gr.
        # food_data[5] -> amount of protein(gr) in 100 gr.
        # food_data[6] -> amount of carbohydrate(gr) in 100 gr.

        # if the food exist in the database then pass.
        if Food.objects.filter(name=food_data[1]):
            pass
        # if the food does not exist in the database then create and save that food to the database.
        else:
            # temporary food to save database.
            # replace ',' with '.' because data is string so when trying to convert
            # string to float ',' character gives a ValueError.
            try:

                temp_food = Food(name=food_data[1], calorie=float(food_data[3].replace(',', '.')),
                                 fat_amount=float(food_data[4].replace(',', '.')),
                                 protein_amount=float(food_data[5].replace(',', '.')),
                                 carbohydrate_amount=float(food_data[6].replace(',', '.')))
                temp_food.save()
            # some values in food_data.csv file does not contain food info and i could not delete them so i catch
            # these values with except.
            except ValueError:
                continue

except FileNotFoundError:
    print('food_data.csv could not find')
