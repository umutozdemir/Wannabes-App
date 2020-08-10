from django.urls import path
from pages.views import*

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('diary', DiaryView.as_view(), name='diary'),
    path('choose_exercise_type', ChooseExerciseType.as_view(), name='choose_exercise_type'),
    path('add_exercise/<int:exercise_type_choose>', AddExerciseView.as_view(), name='add_exercise'),
    path('edit_fitness_profile', EditFitnessProfileView.as_view(), name='edit_fitness_profile'),
    path('add_food', AddFoodView.as_view(), name='add_food'),
    path('delete_food', DeleteFood.as_view(), name='delete_food'),
    path('delete_exercise', DeleteExercise.as_view(), name='delete_exercise'),
]
