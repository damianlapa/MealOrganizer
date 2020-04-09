from django.core.management import BaseCommand


from mealorganizer.management.commands_data.few_recipes_data import INGREDIENT_GROUP_DATA, INGREDIENT_DATA
from mealorganizer.models import Ingredient, IngredientGroup


def add_ingredient_group():
    for name in INGREDIENT_GROUP_DATA:
        IngredientGroup.objects.create(name=name)


def add_ingredients():
    for data in INGREDIENT_DATA:
        group = IngredientGroup.objects.get(name=data[1])
        Ingredient.objects.create(name=data[0], group=group, calories_in_100_grams=data[2],
                                  carbohydrates=data[3], fats=data[4], proteins=data[5])


class Command(BaseCommand):
    help = "Insert few ingredients to data base."

    def handle(self, *args, **kwargs):
        add_ingredient_group()
        add_ingredients()
        print("Data load successfully!")
