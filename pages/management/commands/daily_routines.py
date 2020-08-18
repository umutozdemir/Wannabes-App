from django.core.management.base import BaseCommand
from pages.models import FitnessPerson, ExerciseProgram, DailyPerson, DietProgram
from pages import calculations


class Command(BaseCommand):
    help = 'Resets all of the users daily intakes and creates new exercise program and creates new diet program.'

    def handle(self, *args, **kwargs):
        all_fitness_persons = FitnessPerson.objects.all()
        for fitness_person in all_fitness_persons:
            daily_person = DailyPerson.objects.create(fitness_user=fitness_person)
            daily_person.daily_burned_calories = calculations.calculate_basal_metabolic_rate(fitness_person)
            daily_person.weight = fitness_person.weight
            daily_person.body_mass_index = fitness_person.body_mass_index
            daily_person.body_fat_percentage = fitness_person.body_fat_percentage
            daily_person.save()
            DietProgram.objects.create(daily_person=daily_person)
            ExerciseProgram.objects.create(daily_person=daily_person)
            fitness_person.save()
        self.stdout.write("resetted")
