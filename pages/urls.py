from django.urls import path
from pages.views import*

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('diary', DiaryView.as_view(), name='diary'),
    path('ajax/add_exercise/', AddExerciseView.as_view(), name='add_exercise'),
    path('ajax/add_food/', AddFoodView.as_view(), name='add_food'),
    path('delete_food', DeleteFood.as_view(), name='delete_food'),
    path('delete_exercise', DeleteExercise.as_view(), name='delete_exercise'),
    path('ajax/exercise_selection/', ExerciseSelection.as_view(), name='exercise_selection'),
    path('ajax/food_selection/', FoodSelection.as_view(), name='food_selection'),
    path('ajax/edit_fitness_profile/', EditFitnessProfile.as_view(), name='edit_fitness_profile'),
]
