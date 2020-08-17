import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from pages.forms import *
from django.contrib.auth.decorators import login_required
from pages.models import *
from django.utils import timezone
from django.views import View
from pages import calculations
from django.http import HttpResponse


class HomeView(LoginRequiredMixin, View):
    """ Display homepage with required data."""
    template_name = 'pages/home.html'
    login_url = 'login'
    redirect_field_name = ''

    def get(self, request, *args, **kwargs):
        current_user = request.user
        # if the user login for first time then do calculations.
        if current_user.date_joined.date() == timezone.now().today().date():
            calculations.calculate_daily_required_calorie_intakes(current_user.fitness_person_user)
            calculations.calculate_daily_macros(current_user.fitness_person_user)
            calculations.calculate_body_mass_index(current_user.fitness_person_user)
            calculations.calculate_daily_burned_calories(current_user.fitness_person_user)
            calculations.calculate_body_fat_percentage(current_user.fitness_person_user)
            current_user.fitness_person_user.save()
        fitness_person_of_current_user = current_user.fitness_person_user
        daily_person_of_current_user = fitness_person_of_current_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        context = {'daily_person': daily_person_of_current_user,
                   'fitness_person': fitness_person_of_current_user,
                   'daily_exercise_program': daily_exercise_program_of_current_user,
                   'daily_diet_program': daily_diet_program}
        return render(request, self.template_name, context)


class SignupView(View):
    """ User signup view. """
    form_class = CustomUserForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
            else:
                form.save()
                gender_choice = form.cleaned_data.get('gender_choice')
                age = form.cleaned_data.get('age')
                weight = form.cleaned_data.get('weight')
                height = form.cleaned_data.get('height')
                purpose_of_use = form.cleaned_data.get('purpose_of_use')
                new_user_username = form.cleaned_data.get('username')
                new_user = User.objects.get(username=new_user_username)
                fitness_person = FitnessPerson(user=new_user, gender=gender_choice,
                                               age=age, weight=weight, height=height, purpose_of_use=purpose_of_use)
                fitness_person.save()
                daily_person = DailyPerson.objects.create(fitness_user=fitness_person)
                DietProgram.objects.create(daily_person=daily_person)
                ExerciseProgram.objects.create(daily_person=daily_person)
                fitness_person.save()
                return redirect('home')
        else:
            messages.error(request, 'This username is already taken.')
            return redirect('signup')


class DiaryView(View):
    template_name = 'pages/diary.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        daily_person_of_current_user = current_user.fitness_person_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_user_exercises = daily_exercise_program_of_current_user.userexercise_set.all()
        daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_meals = daily_diet_program.meal_set.all()
        context = {'daily_user_exercises': daily_user_exercises,
                   'daily_meals': daily_meals,
                   'daily_person': daily_person_of_current_user}
        return render(request, self.template_name, context)


class AddExerciseView(View):
    """ This view works with AJAX. User add exercise via this view. """

    def post(self, request, *args, **kwargs):
        exercise_type = int(request.POST.get('exercise_type', int))
        # exercise_type -> 0 means Cardio Exercise
        # exercise_type -> 1 means Weight Exercise
        if exercise_type == 0:
            # current_user is fitness person of the current user.
            current_user = request.user.fitness_person_user
            exercise_id = request.POST.get('exercise_id', int)
            duration = int(request.POST.get('duration', int))
            daily_person_id = request.POST.get('daily_person_id', int)
            daily_exercise_program_id = request.POST.get('daily_exercise_program_id', int)
            how_many_calorie_burn = duration * 6 * 3.5 * current_user.weight / 200
            daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
            daily_exercise_program_of_current_user = ExerciseProgram.objects.get(pk=daily_exercise_program_id)
            exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=Exercise.objects.get(pk=exercise_id),
                duration=duration,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_burned_calories(current_user, daily_person_of_current_user,
                                                         daily_exercise_program_of_current_user)
            daily_person_of_current_user.save()
            current_user.save()
            data = {
                'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
                'message': 'exercise added successfully'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        elif exercise_type == 1:
            # current_user is fitness person of the current user.
            current_user = request.user.fitness_person_user
            exercise_id = request.POST.get('exercise_id', int)
            set_number = int(request.POST.get('set_number', int))
            daily_person_id = request.POST.get('daily_person_id', int)
            daily_exercise_program_id = request.POST.get('daily_exercise_program_id', int)
            rep_number = int(request.POST.get('rep_number', int))
            how_many_calorie_burn = set_number * rep_number * 12
            daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
            daily_exercise_program_of_current_user = ExerciseProgram.objects.get(pk=daily_exercise_program_id)
            exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=Exercise.objects.get(pk=exercise_id),
                set_number=set_number,
                rep_number=rep_number,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_burned_calories(current_user, daily_person_of_current_user,
                                                         daily_exercise_program_of_current_user)
            daily_person_of_current_user.save()
            current_user.save()
            data = {
                'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
                'message': 'exercise added successfully'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")


class AddFoodView(View):
    """ This view works with AJAX. User add food via this view. """

    def post(self, request, *args, **kwargs):
        # current_user is fitness person of the current user.
        current_user = request.user.fitness_person_user
        daily_person_id = request.POST.get('daily_person_id')
        food_id = request.POST.get('food_id')
        daily_diet_program_id = request.POST.get('daily_diet_program_id')
        portion = int(request.POST.get('portion'))
        food_to_add = Food.objects.get(pk=food_id)
        daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
        daily_diet_program = DietProgram.objects.get(pk=daily_diet_program_id)
        user_food_to_add = UserFood.objects.create(diet_program=daily_diet_program,
                                                   food=food_to_add,
                                                   portion=portion)
        daily_person_of_current_user.daily_protein_intake += (food_to_add.protein_amount * portion)
        daily_person_of_current_user.daily_fat_intake += (food_to_add.fat_amount * portion)
        daily_person_of_current_user.daily_carbohydrate_intake += (food_to_add.carbohydrate_amount * portion)
        daily_person_of_current_user.daily_calorie_intakes += (food_to_add.calorie * portion)
        daily_diet_program.save()
        daily_person_of_current_user.save()
        current_user.save()
        data = {
            'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
            'daily_protein_intake': daily_person_of_current_user.daily_protein_intake,
            'daily_fat_intake': daily_person_of_current_user.daily_fat_intake,
            'daily_carbohydrate_intake': daily_person_of_current_user.daily_carbohydrate_intake,
            'message': 'food added successfully'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class DeleteFood(View):
    template_name = 'pages/delete_food.html'

    def get(self, request, *args, **kwargs):
        # current user is fitness person of the current user.
        current_user = request.user.fitness_person_user
        daily_person_of_current_user = current_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        meal_set = daily_diet_program.meal_set.all()
        context = {'meal_set': meal_set}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        deleted_food_selection = request.POST.get('deleted_food_selection').split(',')
        food_id = int(deleted_food_selection[0])
        meal_id = int(deleted_food_selection[1])
        food_to_delete = Food.objects.get(pk=food_id)
        return redirect('diary')


class DeleteExercise(View):
    template_name = 'pages/delete_exercise.html'

    def get(self, request, *args, **kwargs):
        # current user is fitness person of the current user.
        current_user = request.user.fitness_person_user
        daily_person_of_current_user = current_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_exercise_program = daily_person_of_current_user.exerciseprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        context = {'daily_exercise_program': daily_exercise_program}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_exercise_id = int(request.POST.get('deleted_exercise_selection'))
        user_exercise_to_delete = UserExercise.objects.get(pk=user_exercise_id)
        user_exercise_to_delete.delete()
        return redirect('diary')


class ExerciseSelection(View):
    """ This view works with AJAX. Loads appropriate exercises to select2. """

    def get(self, request, *args, **kwargs):
        exercise_type = request.GET.get('exercise_type', int)
        exercises_to_show_in_selection = list(Exercise.objects.filter(exercise_type=exercise_type).annotate(
            text=F('name')).values('id', 'text'))
        data = {
            'exercises_to_show_in_selection': exercises_to_show_in_selection
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class FoodSelection(View):
    """ This view works with AJAX. Loads appropriate foods to select2. """

    def get(self, request, *args, **kwargs):
        foods_to_show_in_selection = list(Food.objects.annotate(text=F('name')).values('id', 'text'))
        data = {
            'foods_to_show_in_selection': foods_to_show_in_selection
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class EditFitnessProfile(View):
    """ This view works with AJAX. User can edit its profile via this view. """

    def post(self, request, *args, **kwargs):
        fitness_person_id = request.POST.get('fitness_person_id', int)
        daily_person_id = request.POST.get('daily_person_id', int)
        weight = int(request.POST.get('weight', int))
        purpose_of_use = int(request.POST.get('purpose_of_use', int))
        fitness_person = FitnessPerson.objects.get(pk=fitness_person_id)
        fitness_person.weight = weight
        fitness_person.purpose_of_use = purpose_of_use
        fitness_person.save()
        daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
        calculations.calculate_daily_required_calorie_intakes(fitness_person)
        calculations.calculate_daily_macros(fitness_person)
        daily_person_of_current_user.body_mass_index = calculations.calculate_body_mass_index(fitness_person)
        daily_person_of_current_user.body_fat_percentage = calculations.calculate_body_fat_percentage(fitness_person)
        daily_person_of_current_user.save()
        fitness_person.save()
        data = {
            'weight': fitness_person.weight,
            'body_mass_index': fitness_person.body_mass_index,
            'body_fat_percentage': fitness_person.body_fat_percentage,
            'required_calorie_intakes': fitness_person.daily_required_calorie_intakes,
            'required_protein_intake': fitness_person.required_protein,
            'required_fat_intake': fitness_person.required_fat,
            'required_carbohydrate_intake': fitness_person.required_carbohydrate
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
