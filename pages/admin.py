from django.contrib import admin
from .models import FitnessPerson, Exercise, Food, ExerciseProgram
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class FitnessPersonInline(admin.StackedInline):
    model = FitnessPerson
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [FitnessPersonInline, ]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('exercise information',
         {'fields': ['name', 'set_number', 'rep_number', 'video_link', 'duration', 'exercise_type']})
    ]


class FoodAdmin(admin.ModelAdmin):
    fieldsets = [
        ('food information',
         {'fields': ['name', 'calorie', 'protein_amount', 'carbohydrate_amount', 'fat_amount', 'recipe_link']})
    ]


class FitnessPersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('info',
         {'fields': ['age', 'weight', 'user', 'height', 'gender']})
    ]


class ExerciseProgramAdmin(admin.ModelAdmin):
    fieldsets = [
        ('info',
         {'fields': ['name', 'exercises']})
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(FitnessPerson, FitnessPersonAdmin)
admin.site.register(ExerciseProgram, ExerciseProgramAdmin)

