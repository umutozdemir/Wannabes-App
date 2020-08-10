# Generated by Django 3.0.8 on 2020-07-23 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0037_auto_20200723_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='duration',
        ),
        migrations.AlterField(
            model_name='exerciseprogram',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
