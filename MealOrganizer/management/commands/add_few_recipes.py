from django.core.management import BaseCommand

from MealOrganizer.management.commands_data.few_recipes_data import RECIPES_DATA
from MealOrganizer.models import Recipe


def add_few_recipes():
    for recipe in RECIPES_DATA:
        new_recipe = Recipe()
        new_recipe.name = recipe[0]
        new_recipe.ingredients = recipe[1]
        new_recipe.description = recipe[2]
        new_recipe.preparation_time = recipe[3]
        new_recipe.save()

class Command(BaseCommand):
    help = "Insert few recipes to data base."

    def handle(self, *args, **kwargs):
        add_few_recipes()
        print("Data load successfully!")
