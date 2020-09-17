from django.core.management import BaseCommand

from mealorganizer.models import Plan, Ingredient, Recipe, RecipePlan, DayName
import random


def add_some_plans(number):
    counter = 0
    while counter < number:
        counter += 1
        name = "Plan nr {}".format(counter)
        new_plan = Plan.objects.create(name=name, description='description')
        meals = ['Śniadanie', 'Drugie śniadanie', 'Obiad', 'Podwieczorek', 'Kolacja']
        order = [1, 2, 3, 4, 5]
        days = DayName.objects.all()
        for day in days:
            for i in range(0, 5):
                new_meal = RecipePlan()
                new_meal.meal_name = meals[i]
                new_meal.order = order[i]
                new_meal.plan = new_plan
                recipes = Recipe.objects.all()
                recipes_list = list(recipes)
                random.shuffle(recipes_list)
                new_meal.recipe = Recipe.objects.get(name=recipes_list[0])
                new_meal.day_name = day

                new_meal.save()


class Command(BaseCommand):
    help = "Insert some plans to data base."

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        add_some_plans(options['number'][0])
        print("Data load successfully!")

