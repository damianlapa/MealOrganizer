# Generated by Django 2.2.6 on 2020-04-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrganizer', '0002_auto_20200407_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='calories_in_100_grams',
            field=models.IntegerField(default=0),
        ),
    ]