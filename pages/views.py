import json

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


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        # if an user login for the first time then do calculations.
        if current_user.date_joined.date() == timezone.now().today().date():
            calculations.calculate_daily_required_calorie_intakes(current_user.fitness_person_user)
            calculations.calculate_daily_macros(current_user.fitness_person_user)
            calculations.calculate_body_mass_index(current_user.fitness_person_user)
            calculations.calculate_daily_burned_calories(current_user.fitness_person_user)
            calculations.calculate_body_fat_percentage(current_user.fitness_person_user)
            current_user.fitness_person_user.save()
        daily_person_of_current_user = current_user.fitness_person_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        food_set = Food.objects.all()
        daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        context = {'daily_person': daily_person_of_current_user,
                   'food_set': food_set,
                   'daily_exercise_program': daily_exercise_program_of_current_user,
                   'daily_diet_program': daily_diet_program}
        return render(request, self.template_name, context)


class SignupView(View):
    form_class = CustomUserForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
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
            return redirect('signup')


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class AddExerciseView(View):

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
            daily_person_of_current_user.save()
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_required_calorie_intakes(current_user)
            calculations.calculate_daily_macros(current_user)
            calculations.calculate_body_mass_index(current_user)
            calculations.calculate_daily_burned_calories(current_user)
            current_user.save()
            data = {
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
            daily_person_of_current_user.save()
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_required_calorie_intakes(current_user)
            calculations.calculate_daily_macros(current_user)
            calculations.calculate_body_mass_index(current_user)
            calculations.calculate_daily_burned_calories(current_user)
            current_user.save()
            data = {
                'message': 'exercise added successfully'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")


def login(request):
    return render(request, 'registration/login.html')


@method_decorator(login_required, name='dispatch')
class EditFitnessProfileView(View):
    template_name = 'pages/edit_fitness_profile.html'
    form_class = EditFitnessProfileForm

    def get(self, request, *args, **kwargs):
        edit_fitness_profile_form = self.form_class
        return render(request, self.template_name, {'form': edit_fitness_profile_form})

    def post(self, request, *args, **kwargs):
        edit_fitness_profile_form = self.form_class(request.POST)
        if edit_fitness_profile_form.is_valid():
            current_fitness_person = request.user.fitness_person_user
            age = edit_fitness_profile_form.cleaned_data.get('age')
            weight = edit_fitness_profile_form.cleaned_data.get('weight')
            height = edit_fitness_profile_form.cleaned_data.get('height')
            current_fitness_person.age = age
            current_fitness_person.weight = weight
            current_fitness_person.height = height
            calculations.calculate_daily_required_calorie_intakes(current_fitness_person)
            calculations.calculate_daily_macros(current_fitness_person)
            calculations.calculate_body_mass_index(current_fitness_person)
            calculations.calculate_daily_burned_calories(current_fitness_person)
            calculations.calculate_body_fat_percentage(current_fitness_person)
            current_fitness_person.save()
            return redirect('diary')


@method_decorator(login_required, name='dispatch')
class AddFoodView(View):

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
        daily_person_of_current_user.save()
        daily_diet_program.save()
        calculations.calculate_daily_required_calorie_intakes(current_user)
        calculations.calculate_daily_macros(current_user)
        calculations.calculate_body_mass_index(current_user)
        calculations.calculate_daily_burned_calories(current_user)
        current_user.save()
        data = {
            'message': 'food added successfully'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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

    def get(self, request, *args, **kwargs):
        exercise_type = request.GET.get('exercise_type', int)
        exercises_to_show_in_selection = list(Exercise.objects.filter(exercise_type=exercise_type).annotate(
            text=F('name')).values('id', 'text'))
        data = {
            'exercises_to_show_in_selection': exercises_to_show_in_selection
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class FoodSelection(View):

    def get(self, request, *args, **kwargs):
        foods_to_show_in_selection = list(Food.objects.annotate(text=F('name')).values('id', 'text'))
        data = {
            'foods_to_show_in_selection': foods_to_show_in_selection
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
