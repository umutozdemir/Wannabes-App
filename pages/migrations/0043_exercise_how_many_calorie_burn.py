# Generated by Django 3.0.8 on 2020-07-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0042_remove_exercise_how_many_calorie_burn'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='how_many_calorie_burn',
            field=models.IntegerField(null=True),
        ),
    ]
