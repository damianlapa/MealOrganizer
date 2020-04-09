from django.core.management import BaseCommand

from mealorganizer.management.commands_data.few_recipes_data import PLAN_DATA
from mealorganizer.models import Plan
import random


def add_some_plans():
    for plan in PLAN_DATA:
        new_plan = Plan()
        new_plan.name = plan[0]
        new_plan.description = plan[1]
        new_plan.save()

class Command(BaseCommand):
    help = "Insert some plans to data base."

    def handle(self, *args, **kwargs):
        add_some_plans()
        print("Data load successfully!")

