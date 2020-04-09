from django.core.management import BaseCommand

from mealorganizer.management.commands_data.few_recipes_data import RECIPES_DATA
from mealorganizer.models import Recipe
import random


class Command(BaseCommand):
    help = "Fill Recipe votes (random)."

    def handle(self, *args, **kwargs):
        recipes = Recipe.objects.filter(votes=0)
        for r in recipes:
            r.votes = random.randint(0,1000)
            r.save()

        cnt = recipes.count()

        self.stdout.write(self.style.SUCCESS('Operation completed! Filled recipes: {}'.format(cnt)))

