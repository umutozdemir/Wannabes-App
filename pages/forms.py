from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from pages.models import FitnessPerson


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    GENDER_CHOICE = (
        (0, 'Male'),
        (1, 'Female'),
    )
    gender_choice = forms.ChoiceField(required=True, choices=GENDER_CHOICE)
    weight = forms.FloatField(required=True, help_text='please enter in kg')
    height = forms.FloatField(required=True, help_text='please enter in meter')
    PURPOSE_CHOICE = (
        (0, 'I want to keep my weight.'),
        (1, 'I want to lose weight.'),
        (2, 'I want to gain weight'),
    )
    purpose_of_use = forms.ChoiceField(required=True, choices=PURPOSE_CHOICE)
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email exists")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",
                  "age", "gender_choice", "weight", "height", "purpose_of_use")


class WeightExerciseForm(forms.Form):
    set_number = forms.IntegerField(label='set number')
    rep_number = forms.IntegerField(label='rep number')


class CardioExerciseForm(forms.Form):
    duration = forms.IntegerField(label='Duration', widget=forms.TextInput(attrs={'placeholder': 'in minutes'}))
    exercise_selection = forms.Select


class ExerciseTypeSelectionForm(forms.Form):
    EXERCISE_CHOISES = (
        (0, 'Cardio'),
        (1, 'Weight'),
    )
    exercise_type = forms.ChoiceField(choices=EXERCISE_CHOISES)


class FitnessProfileForm(ModelForm):
    class Meta:
        model = FitnessPerson
        fields = ("age", "weight", "height", "gender", "purpose_of_use")
        widgets = {
            'weight': forms.TextInput(attrs={'placeholder': 'in kg'}),
            'height': forms.TextInput(attrs={'placeholder': 'in meter'})
        }


class EditFitnessProfileForm(forms.Form):
    age = forms.IntegerField(label='Age')
    weight = forms.FloatField(required=True, widget=forms.TextInput(attrs={'placeholder': 'in kg'}), label='Weight')
    height = forms.FloatField(required=True, widget=forms.TextInput(attrs={'placeholder': 'in meter'}), label='Height')
    PURPOSE_CHOICE = (
        (0, 'I want to keep my weight.'),
        (1, 'I want to lose weight.'),
        (2, 'I want to gain weight'),
    )
    purpose_of_use = forms.ChoiceField(required=True, choices=PURPOSE_CHOICE)


class AddFoodForm(forms.Form):
    portion = forms.IntegerField(label='Portion')
