from django.db import models
from django.contrib.auth.models import User


class FitnessPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fitness_person_user')
    age = models.IntegerField(default=0)
    # weight should be in kg.
    weight = models.FloatField()
    # height should be in meter.
    height = models.FloatField()
    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'),
                      )
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    KEEP_WEIGHT = 0
    LOSE_WEIGHT = 1
    GAIN_WEIGHT = 2
    PURPOSE_CHOICES = (
        (KEEP_WEIGHT, 'I want to keep my weight.'),
        (LOSE_WEIGHT, 'I want to lose weight.'),
        (GAIN_WEIGHT, 'I want to gain weight'),
    )
    purpose_of_use = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES, null=True)
    body_fat_percentage = models.FloatField(null=True, blank=True)
    body_mass_index = models.FloatField(null=True, blank=True)
    daily_required_calorie_intakes = models.IntegerField(null=True, blank=True)
    required_carbohydrate = models.IntegerField(null=True, blank=True)
    required_protein = models.IntegerField(null=True, blank=True)
    required_fat = models.IntegerField(null=True, blank=True)
    neck = models.IntegerField(null=True, blank=True)
    waist = models.IntegerField(null=True, blank=True)
    hip = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Food(models.Model):
    name = models.CharField(max_length=500)
    # calorie in 100 gr.
    calorie = models.FloatField()
    protein_amount = models.FloatField()
    carbohydrate_amount = models.FloatField()
    fat_amount = models.FloatField()
    recipe_link = models.URLField(null=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    CARDIO = 0
    WEIGHT_EXERCISE = 1
    EXERCISE_TYPE = (
        (CARDIO, 'Cardio'),
        (WEIGHT_EXERCISE, 'Weight Exercise'),
    )
    exercise_type = models.PositiveSmallIntegerField(choices=EXERCISE_TYPE, default=1)
    video_link = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class DailyPerson(models.Model):
    fitness_user = models.ForeignKey(FitnessPerson, on_delete=models.CASCADE)
    daily_calorie_intakes = models.IntegerField(default=0, blank=True)
    daily_burned_calories = models.IntegerField(default=0, blank=True)
    daily_protein_intake = models.IntegerField(default=0, blank=True)
    daily_carbohydrate_intake = models.IntegerField(default=0, blank=True)
    daily_fat_intake = models.IntegerField(default=0, blank=True)
    date_added = models.DateTimeField('day added', auto_now_add=True, null=True)


# ExerciseProgram is collection of exercises, every ExerciseProgram belongs a certain day.
class ExerciseProgram(models.Model):
    daily_person = models.ForeignKey(DailyPerson, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField('day added', auto_now_add=True, null=True)


class UserExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)
    exercise_program = models.ForeignKey(ExerciseProgram, on_delete=models.CASCADE)
    set_number = models.IntegerField(default=0)
    rep_number = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    how_many_calorie_burn = models.IntegerField(default=0)


# Diet program is a collection of foods.
class DietProgram(models.Model):
    daily_person = models.ForeignKey(DailyPerson, on_delete=models.CASCADE)
    date_added = models.DateTimeField('day added', auto_now_add=True, null=True)
    foods = models.ManyToManyField(Food)
