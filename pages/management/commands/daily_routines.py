from django.core.management.base import BaseCommand
from pages.models import FitnessPerson, ExerciseProgram, DailyPerson, DietProgram


class Command(BaseCommand):
    help = 'Resets all of the users daily intakes and creates new exercise program and creates new meal.'

    def handle(self, *args, **kwargs):
        all_fitness_persons = FitnessPerson.objects.all()
        for fitness_person in all_fitness_persons:
            daily_person = DailyPerson.objects.create(fitness_user=fitness_person)
            DietProgram.objects.create(daily_person=daily_person)
            ExerciseProgram.objects.create(daily_person=daily_person)
            fitness_person.save()
        self.stdout.write("resetted")
