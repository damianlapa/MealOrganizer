# Generated by Django 2.2.10 on 2020-04-10 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealorganizer', '0002_auto_20200408_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation_method',
            field=models.TextField(default='text'),
            preserve_default=False,
        ),
    ]