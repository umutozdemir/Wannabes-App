# Generated by Django 3.0.8 on 2020-07-27 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0049_auto_20200727_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexercise',
            name='fitness_user',
        ),
        migrations.RemoveField(
            model_name='userexercise',
            name='exercise',
        ),
        migrations.AddField(
            model_name='userexercise',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Exercise'),
        ),
    ]
