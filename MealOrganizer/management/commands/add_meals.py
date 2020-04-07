from django.core.management import BaseCommand
from MealOrganizer.models import RecipePlan, Plan, Recipe
import random

MEALS =(
    (1, "Śniadanie"),
    (2, "Drugie Śniadanie"),
    (3, "Obiad"),
    (4, "Podwieczorek"),
    (5, "Kolacja")
)

def add_meals():
    for plan in Plan.objects.all():
        for plan.meal in MEALS:
            RecipePlan.objects.create(meal_name=plan.meal[1], order=plan.meal[0], recipe_id=random.randint(1, 30),
                                          plan_id=random.randint(1, 16), day_name_id=random.randint(6, 12))

class Command(BaseCommand):
    help = "Insert meals to data base."

    def handle(self, *args, **kwargs):
        add_meals()
        print("Data load successfully!")



