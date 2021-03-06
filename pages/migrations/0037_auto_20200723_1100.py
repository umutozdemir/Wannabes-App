# Generated by Django 3.0.8 on 2020-07-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0036_auto_20200723_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciseprogram',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='exerciseprogram',
            name='how_many_calorie_burn',
        ),
        migrations.RemoveField(
            model_name='exerciseprogram',
            name='rep_number',
        ),
        migrations.RemoveField(
            model_name='exerciseprogram',
            name='set_number',
        ),
        migrations.AddField(
            model_name='exercise',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exercise',
            name='how_many_calorie_burn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='rep_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exercise',
            name='set_number',
            field=models.IntegerField(default=0),
        ),
    ]
