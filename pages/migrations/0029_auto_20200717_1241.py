# Generated by Django 3.0.8 on 2020-07-17 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0028_auto_20200716_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='food',
            name='date_added',
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(null=True, verbose_name='day added')),
                ('foods', models.ManyToManyField(to='pages.Food')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meal_program', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(null=True, verbose_name='day added')),
                ('exercises', models.ManyToManyField(to='pages.Exercise')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_program', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
