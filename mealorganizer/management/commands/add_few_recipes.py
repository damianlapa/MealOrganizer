from django.core.management import BaseCommand
import random
from mealorganizer.models import Recipe, Ingredient, IngredientGroup, IngredientWeight


def add_few_recipes(number):
    counter = 0
    while counter < number:
        ingredients = Ingredient.objects.all()
        ingredients_list = []
        for ingredient in ingredients:
            ingredients_list.append(ingredient)
        random.shuffle(ingredients_list)
        new_recipe = Recipe()
        new_recipe_ingredients = []
        for _ in range(3):
            new_recipe_ingredients.append(ingredients_list.pop(0))
        name = "{} with {} and {}".format(new_recipe_ingredients[0], new_recipe_ingredients[1],
                                          new_recipe_ingredients[2])
        try:
            Recipe.objects.get(name=name)
        except Recipe.DoesNotExist:
            new_recipe.name = name
            new_recipe.preparation_time = random.randint(1, 18) * 5
            new_recipe.description = 'description'
            new_recipe.preparation_method = 'preparation method'
            new_recipe.votes = random.randint(-10, 10)

            new_recipe.save()

            for ingredient in new_recipe_ingredients:
                ingredient = Ingredient.objects.get(name=ingredient)
                weight = random.randint(5, 20) * 10
                IngredientWeight.objects.create(ingredient=ingredient, weight_in_grams=weight, recipe=new_recipe)

            counter += 1


class Command(BaseCommand):
    help = "Insert few recipes to data base."

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        add_few_recipes(options['number'][0])
        print("Data load successfully!")
