# Generated by Django 3.0.8 on 2020-07-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0040_auto_20200723_1341'),
    ]

    operations = [
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
