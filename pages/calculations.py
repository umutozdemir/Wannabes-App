from pages.models import *
from django.utils import timezone
import math


def calculate_body_fat_percentage(fitness_person):
    if fitness_person.gender == FitnessPerson.MALE:
        fitness_person.body_fat_percentage = (1.2 * fitness_person.body_mass_index) + (0.23 * fitness_person.age) - 16.2
    elif fitness_person.gender == FitnessPerson.FEMALE:
        fitness_person.body_fat_percentage = (1.2 * fitness_person.body_mass_index) + (0.23 * fitness_person.age) - 5.4


def calculate_body_mass_index(fitness_person):
    fitness_person.body_mass_index = fitness_person.weight / (fitness_person.height * fitness_person.height)


def calculate_daily_required_calorie_intakes(fitness_person):
    basal_metabolic_rate = calculate_basal_metabolic_rate(fitness_person)
    if fitness_person.purpose_of_use == FitnessPerson.KEEP_WEIGHT:
        fitness_person.daily_required_calorie_intakes = basal_metabolic_rate + 500
    elif fitness_person.purpose_of_use == FitnessPerson.LOSE_WEIGHT:
        fitness_person.daily_required_calorie_intakes = basal_metabolic_rate
    elif fitness_person.purpose_of_use == FitnessPerson.GAIN_WEIGHT:
        fitness_person.daily_required_calorie_intakes = basal_metabolic_rate + 1000


def calculate_daily_macros(fitness_person):
    if fitness_person.daily_required_calorie_intakes is not None:
        fitness_person.required_carbohydrate = fitness_person.daily_required_calorie_intakes * 45 / 450
        fitness_person.required_protein = fitness_person.daily_required_calorie_intakes * 30 / 400
        fitness_person.required_fat = fitness_person.daily_required_calorie_intakes * 25 / 930


def calculate_daily_burned_calories(fitness_person):
    current_day = timezone.now().today().date()
    daily_person = fitness_person.dailyperson_set.filter(date_added__date=current_day)[0]
    daily_exercise_program = daily_person.exerciseprogram_set.filter(date_added__date=current_day)[0]
    exercises_did_today = daily_exercise_program.userexercise_set.all()
    basal_metabolic_rate = calculate_basal_metabolic_rate(fitness_person)
    sum_of_burned_calories = basal_metabolic_rate
    for exercise in exercises_did_today:
        sum_of_burned_calories += exercise.how_many_calorie_burn
    daily_person.daily_burned_calories = sum_of_burned_calories
    daily_person.save()
    fitness_person.save()


def calculate_basal_metabolic_rate(fitness_person):
    basal_metabolic_rate = (10 * fitness_person.weight) + (625 * fitness_person.height) - (5 * fitness_person.age) + 5
    if fitness_person.gender == FitnessPerson.FEMALE:
        basal_metabolic_rate = basal_metabolic_rate - 166
    return basal_metabolic_rate
