from django.core.management import BaseCommand
from mealorganizer.models import DayName

WEEKDAYS = (
    (1, "Poniedziałek"),
    (2, "Wtorek"),
    (3, "Środa"),
    (4, "Czwartek"),
    (5, "Piątek"),
    (6, "Sobota"),
    (7, "Niedziela")
)


def add_week_days():
    for row in WEEKDAYS:
        DayName.objects.create(name=row[1], order=row[0])

class Command(BaseCommand):
    help = "Insert week days to data base."

    def handle(self, *args, **kwargs):
        add_week_days()
        print("Data load successfully!")