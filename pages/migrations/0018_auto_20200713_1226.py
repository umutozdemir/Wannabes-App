# Generated by Django 3.0.8 on 2020-07-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20200713_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessperson',
            name='exercises',
        ),
        migrations.AddField(
            model_name='fitnessperson',
            name='exercises',
            field=models.ManyToManyField(blank=True, null=True, to='pages.Exercise'),
        ),
        migrations.RemoveField(
            model_name='fitnessperson',
            name='foods',
        ),
        migrations.AddField(
            model_name='fitnessperson',
            name='foods',
            field=models.ManyToManyField(blank=True, null=True, to='pages.Food'),
        ),
    ]
