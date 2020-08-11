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
from django.http import JsonResponse, HttpResponse


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        daily_person_of_current_user = current_user.fitness_person_user.dailyperson_set.filter(
            date_added__date=timezone.now().today().date())[0]
        food_set = Food.objects.all()
        context = {'daily_person': daily_person_of_current_user,
                   'food_set': food_set}
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
            neck = form.cleaned_data.get('neck')
            waist = form.cleaned_data.get('waist')
            hip = form.cleaned_data.get('hip')
            purpose_of_use = form.cleaned_data.get('purpose_of_use')
            new_user_username = form.cleaned_data.get('username')
            new_user = User.objects.get(username=new_user_username)
            fitness_person = FitnessPerson(user=new_user, gender=gender_choice,
                                           age=age, weight=weight, height=height, purpose_of_use=purpose_of_use,
                                           neck=neck, waist=waist, hip=hip)
            fitness_person.save()
            daily_person = DailyPerson.objects.create(fitness_user=fitness_person)
            DietProgram.objects.create(daily_person=daily_person)
            ExerciseProgram.objects.create(daily_person=daily_person)
            fitness_person.save()
            return redirect('login')
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
class ChooseExerciseType(View):
    template_name = 'pages/choose_exercise_type.html'
    form_class = ExerciseTypeSelectionForm

    def get(self, request, *args, **kwargs):
        exercise_type_selection_form = self.form_class
        context = {'form': exercise_type_selection_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        exercise_type_selection_form = self.form_class(request.POST)
        exercise_type_choose = exercise_type_selection_form.data['exercise_type']
        return redirect('add_exercise/' + exercise_type_choose)


@method_decorator(login_required, name='dispatch')
class AddExerciseView(View):
    template_name = 'pages/add_exercise.html'
    form_classes = {
        'cardio_exercise_form': CardioExerciseForm,
        'weight_exercise_form': WeightExerciseForm
    }
    exercise_type_choose = None

    def get_object(self, queryset=None):
        return queryset.get(exercise_type_choose=self.exercise_type_choose)

    def get(self, request, *args, **kwargs):
        # exercise_type_choose = 0 means user want to add cardio exercise.
        # exercise_type_choose = 1 means user want to add weight exercise.
        self.exercise_type_choose = self.kwargs['exercise_type_choose']
        # Query exercises from database with respect to its exercise type.
        exercises = Exercise.objects.filter(exercise_type=self.exercise_type_choose)
        # list of exercise names from queried data.
        exercise_name_list = [exercise.name for exercise in exercises]
        # user want to add cardio exercise so context is cardio exercise form and exercises name list
        # that contains cardio exercises.
        if int(self.exercise_type_choose) == 0:
            form = self.form_classes['cardio_exercise_form']
            context = {'exercise_name_list': exercise_name_list, 'form': form}
            return render(request, 'pages/add_exercise.html', context)
        # user want to add weight exercise so context is weight exercise form and exercises name list
        # that contains weight exercises.
        elif int(self.exercise_type_choose) == 1:
            form = self.form_classes['weight_exercise_form']
            context = {'exercise_name_list': exercise_name_list, 'form': form}
            return render(request, 'pages/add_exercise.html', context)

    def post(self, request, *args, **kwargs):
        cardio_exercise_form = self.form_classes['cardio_exercise_form'](request.POST)
        weight_exercise_form = self.form_classes['weight_exercise_form'](request.POST)
        # if the user post cardio exercise form.
        if cardio_exercise_form.is_valid():
            # current_user is fitness person of the current user.
            current_user = request.user.fitness_person_user
            exercise_name = request.POST.get('exercise_selection')
            duration = cardio_exercise_form.cleaned_data.get('duration')
            how_many_calorie_burn = duration * 6 * 3.5 * current_user.weight / 200
            daily_person_of_current_user = current_user.dailyperson_set.filter(
                date_added__date=timezone.now().today().date())[0]
            daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
                date_added__date=timezone.now().today().date())[0]
            exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=Exercise.objects.get(name=exercise_name),
                duration=duration,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_person_of_current_user.save()
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_required_calorie_intakes(current_user)
            calculations.calculate_daily_macros(current_user)
            calculations.calculate_body_mass_index(current_user)
            calculations.calculate_daily_burned_calories(current_user)
            calculations.calculate_body_fat_percentage(current_user)
            current_user.save()
            return redirect('diary')
        # if the user post weight exercise form.
        elif weight_exercise_form.is_valid():
            # current_user is fitness person of the current user.
            current_user = request.user.fitness_person_user
            exercise_name = request.POST.get('exercise_selection')
            set_number = weight_exercise_form.cleaned_data.get('set_number')
            rep_number = weight_exercise_form.cleaned_data.get('rep_number')
            how_many_calorie_burn = set_number * rep_number * 12
            daily_person_of_current_user = current_user.dailyperson_set.filter(
                date_added__date=timezone.now().today().date())[0]
            daily_exercise_program_of_current_user = daily_person_of_current_user.exerciseprogram_set.filter(
                date_added__date=timezone.now().today().date())[0]
            exercise_to_add = UserExercise.objects.create(
                exercise_program=daily_exercise_program_of_current_user,
                exercise=Exercise.objects.get(name=exercise_name),
                set_number=set_number,
                rep_number=rep_number,
                how_many_calorie_burn=how_many_calorie_burn)
            daily_person_of_current_user.save()
            daily_exercise_program_of_current_user.save()
            calculations.calculate_daily_required_calorie_intakes(current_user)
            calculations.calculate_daily_macros(current_user)
            calculations.calculate_body_mass_index(current_user)
            calculations.calculate_daily_burned_calories(current_user)
            calculations.calculate_body_fat_percentage(current_user)
            current_user.save()
            return redirect('diary')
        else:
            return redirect('home')


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
            neck = edit_fitness_profile_form.cleaned_data.get('neck')
            waist = edit_fitness_profile_form.cleaned_data.get('waist')
            hip = edit_fitness_profile_form.cleaned_data.get('hip')
            current_fitness_person.age = age
            current_fitness_person.weight = weight
            current_fitness_person.height = height
            current_fitness_person.neck = neck
            current_fitness_person.waist = waist
            current_fitness_person.hip = hip
            calculations.calculate_daily_required_calorie_intakes(current_fitness_person)
            calculations.calculate_daily_macros(current_fitness_person)
            calculations.calculate_body_mass_index(current_fitness_person)
            calculations.calculate_daily_burned_calories(current_fitness_person)
            calculations.calculate_body_fat_percentage(current_fitness_person)
            current_fitness_person.save()
            return redirect('diary')


@method_decorator(login_required, name='dispatch')
class AddFoodView(View):
    template_name = 'pages/add_food.html'
    form_class = AddFoodForm

    def get(self, request, *args, **kwargs):
        food_set = Food.objects.all()
        add_food_form = self.form_class
        context = {'food_set': food_set, 'form': add_food_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        add_food_form = self.form_class(request.POST)
        if add_food_form.is_valid():
            # current_user is fitness person of the current user.
            current_user = request.user.fitness_person_user
            food_id = int(request.POST.get('food_selection'))
            portion = add_food_form.cleaned_data.get('portion')
            food_to_add = Food.objects.get(pk=food_id)
            daily_person_of_current_user = current_user.dailyperson_set.filter(
                date_added__date=timezone.now().today().date())[0]
            daily_diet_program = daily_person_of_current_user.dietprogram_set.filter(
                date_added__date=timezone.now().today().date())[0]
            new_meal = Meal.objects.create(fitness_user=current_user, diet_program=daily_diet_program)
            new_meal.foods.add(food_to_add)
            new_meal.save()
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
        return redirect('diary')


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
        meal = Meal.objects.get(pk=meal_id)
        food_to_delete = Food.objects.get(pk=food_id)
        meal.foods.remove(food_to_delete)
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
        print(exercises_to_show_in_selection[0])
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
