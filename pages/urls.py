from django.urls import path
from pages.views import*

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('ajax/add_exercise/', AddExerciseView.as_view(), name='add_exercise'),
    path('ajax/add_food/', AddFoodView.as_view(), name='add_food'),
    path('ajax/exercise_selection/', ExerciseSelection.as_view(), name='exercise_selection'),
    path('ajax/food_selection/', FoodSelection.as_view(), name='food_selection'),
    path('ajax/edit_fitness_profile/', EditFitnessProfile.as_view(), name='edit_fitness_profile'),
    path('ajax/delete_exercise/', DeleteExercise.as_view(), name='delete_exercise'),
    path('ajax/delete_food/', DeleteFood.as_view(), name='delete_food'),
]
