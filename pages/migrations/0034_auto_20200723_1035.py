# Generated by Django 3.0.8 on 2020-07-23 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0033_auto_20200723_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='how_many_calorie_burn',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='rep_number',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='set_number',
        ),
        migrations.RemoveField(
            model_name='exerciseprogram',
            name='name',
        ),
        migrations.RemoveField(
            model_name='fitnessperson',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='fitnessperson',
            name='foods',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='meal_name',
        ),
        migrations.AddField(
            model_name='exerciseprogram',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exerciseprogram',
            name='how_many_calorie_burn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='exerciseprogram',
            name='rep_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exerciseprogram',
            name='set_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fitnessperson',
            name='exercise_programs',
            field=models.ManyToManyField(blank=True, to='pages.ExerciseProgram'),
        ),
        migrations.AddField(
            model_name='fitnessperson',
            name='meals',
            field=models.ManyToManyField(blank=True, to='pages.Meal'),
        ),
    ]
