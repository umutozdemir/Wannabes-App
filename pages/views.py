import json


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from pages.forms import *
from pages.models import *
from django.utils import timezone
from django.views import View
from pages import calculations
from django.http import HttpResponse


class HomeView(LoginRequiredMixin, View):
    """ Display homepage with appropriate context."""
    template_name = 'pages/home.html'
    login_url = 'login'
    redirect_field_name = ''

    def get(self, request, *args, **kwargs):
        current_user = request.user
        fitness_person_of_current_user = current_user.fitness_person_user
        daily_person_of_current_user = fitness_person_of_current_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
            date_added__date=timezone.now().today().date())[0]
        # first object of set is oldest daily_person, last object of set is newest daily_person
        # last_seven_days arrays length might be less than 7.
        last_seven_days_daily_persons = DailyPerson.objects.filter(fitness_user=fitness_person_of_current_user)[:7]
        last_seven_days_weight = []
        last_seven_days_calorie_intakes = []
        last_seven_days_burned_calories = []
        for daily_person in last_seven_days_daily_persons:
            last_seven_days_weight.append(daily_person.weight)
            last_seven_days_calorie_intakes.append(daily_person.daily_calorie_intakes)
            last_seven_days_burned_calories.append(daily_person.daily_burned_calories)

        # if the user login for first time then do calculations.
        if current_user.date_joined.date() == timezone.now().today().date():
            calculations.calculate_daily_required_calorie_intakes(current_user.fitness_person_user)
            calculations.calculate_daily_macros(current_user.fitness_person_user)
            calculations.calculate_body_mass_index(current_user.fitness_person_user)
            daily_person_of_current_user.daily_burned_calories = calculations.calculate_basal_metabolic_rate(
                fitness_person_of_current_user)
            calculations.calculate_body_fat_percentage(current_user.fitness_person_user)
            current_user.fitness_person_user.save()
        context = {'daily_person': daily_person_of_current_user,
                   'fitness_person': fitness_person_of_current_user,
                   'daily_exercise_program': daily_exercise_program_of_current_user,
                   'daily_diet_program': daily_diet_program,
                   'last_seven_days_weight': last_seven_days_weight,
                   'last_seven_days_calorie_intakes': last_seven_days_calorie_intakes,
                   'last_seven_days_burned_calories': last_seven_days_burned_calories}
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
                daily_person = DailyPerson.objects.create(fitness_user=fitness_person, weight=weight)
                DietProgram.objects.create(daily_person=daily_person)
                ExerciseProgram.objects.create(daily_person=daily_person)
                fitness_person.save()
                return redirect('home')
        else:
            messages.error(request, 'This username is already taken.')
            return redirect('signup')


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
            exercise_to_add = Exercise.objects.get(pk=exercise_id)
            how_many_calorie_burn = int(duration * 6 * 3.5 * current_user.weight / 200)
            daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
            daily_exercise_program_of_current_user = ExerciseProgram.objects.get(pk=daily_exercise_program_id)
            user_exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=exercise_to_add,
                duration=duration,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_exercise_program_of_current_user.save()
            daily_person_of_current_user.daily_burned_calories += how_many_calorie_burn
            daily_person_of_current_user.save()
            current_user.save()
            data = {
                'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
                'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
                'user_exercise_id': user_exercise_to_add.id,
                'how_many_calorie_burn': how_many_calorie_burn,
                'exercise_video_link': exercise_to_add.video_link
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
            exercise_to_add = Exercise.objects.get(pk=exercise_id)
            user_exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=exercise_to_add,
                set_number=set_number,
                rep_number=rep_number,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_exercise_program_of_current_user.save()
            daily_person_of_current_user.daily_burned_calories += how_many_calorie_burn
            daily_person_of_current_user.save()
            current_user.save()
            data = {
                'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
                'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
                'user_exercise_id': user_exercise_to_add.id,
                'how_many_calorie_burn': how_many_calorie_burn,
                'exercise_video_link': exercise_to_add.video_link
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
        daily_person_of_current_user.daily_protein_intake += int((food_to_add.protein_amount * portion))
        daily_person_of_current_user.daily_fat_intake += int((food_to_add.fat_amount * portion))
        daily_person_of_current_user.daily_carbohydrate_intake += int((food_to_add.carbohydrate_amount * portion))
        daily_person_of_current_user.daily_calorie_intakes += int((food_to_add.calorie * portion))
        daily_diet_program.save()
        daily_person_of_current_user.save()
        current_user.save()
        data = {
            'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
            'daily_protein_intake': daily_person_of_current_user.daily_protein_intake,
            'daily_fat_intake': daily_person_of_current_user.daily_fat_intake,
            'daily_carbohydrate_intake': daily_person_of_current_user.daily_carbohydrate_intake,
            'user_food_id': user_food_to_add.id,
            'food_calorie': food_to_add.calorie,
            'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
            'food_recipe_link': food_to_add.recipe_link
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


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
        weight = float(request.POST.get('weight', int))
        purpose_of_use = int(request.POST.get('purpose_of_use', int))
        fitness_person = FitnessPerson.objects.get(pk=fitness_person_id)
        fitness_person.weight = weight
        fitness_person.purpose_of_use = purpose_of_use
        fitness_person.save()
        daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
        daily_person_of_current_user.weight = weight
        calculations.calculate_daily_required_calorie_intakes(fitness_person)
        calculations.calculate_daily_macros(fitness_person)
        daily_person_of_current_user.body_mass_index = calculations.calculate_body_mass_index(fitness_person)
        daily_person_of_current_user.body_fat_percentage = calculations.calculate_body_fat_percentage(fitness_person)
        daily_person_of_current_user.save()
        fitness_person.save()
        data = {
            'message': 'Profile updated successfully',
            'weight': fitness_person.weight,
            'body_mass_index': fitness_person.body_mass_index,
            'body_fat_percentage': fitness_person.body_fat_percentage,
            'required_calorie_intakes': fitness_person.daily_required_calorie_intakes,
            'required_protein_intake': fitness_person.required_protein,
            'required_fat_intake': fitness_person.required_fat,
            'required_carbohydrate_intake': fitness_person.required_carbohydrate
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class DeleteExercise(View):
    """ This view works with AJAX. User can delete an exercise via this view. """

    def post(self, request, *args, **kwargs):
        user_exercise_id = request.POST.get('user_exercise_id', int)
        daily_person_id = request.POST.get('daily_person_id', int)
        user_exercise_to_delete = UserExercise.objects.get(pk=user_exercise_id)
        daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
        daily_person_of_current_user.daily_burned_calories -= user_exercise_to_delete.how_many_calorie_burn
        daily_person_of_current_user.save()
        user_exercise_to_delete.delete()
        data = {
            'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
            'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
            'message': 'Exercise deleted with success'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class DeleteFood(View):
    """ This view works with AJAX. User can delete a food via this view. """

    def post(self, request, *args, **kwargs):
        user_food_id = request.POST.get('user_food_id', int)
        daily_person_id = request.POST.get('daily_person_id', int)
        user_food_to_delete = UserFood.objects.get(pk=user_food_id)
        portion = user_food_to_delete.portion
        daily_person_of_current_user = DailyPerson.objects.get(pk=daily_person_id)
        food = user_food_to_delete.food
        daily_person_of_current_user.daily_calorie_intakes -= int((food.calorie * portion))
        daily_person_of_current_user.daily_protein_intake -= int((food.protein_amount * portion))
        daily_person_of_current_user.daily_fat_intake -= int((food.fat_amount * portion))
        daily_person_of_current_user.daily_carbohydrate_intake -= int((food.carbohydrate_amount * portion))
        daily_person_of_current_user.save()
        user_food_to_delete.delete()
        data = {
            'daily_calorie_intakes': daily_person_of_current_user.daily_calorie_intakes,
            'daily_burned_calories': daily_person_of_current_user.daily_burned_calories,
            'daily_protein_intake': daily_person_of_current_user.daily_protein_intake,
            'daily_fat_intake': daily_person_of_current_user.daily_fat_intake,
            'daily_carbohydrate_intake': daily_person_of_current_user.daily_carbohydrate_intake,
            'message': 'Food deleted with success'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
