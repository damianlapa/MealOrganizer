from django.db import models

DayText = (
    ('Poniedziałek', 'Poniedziałek'),
    ('Wtorek', 'Wtorek'),
    ('Sroda', 'Środa'),
    ('Czwartek', 'Czwartek'),
    ('Piątek', 'Piątek'),
    ('Sobota', 'Sobota'),
    ('Niedziela', 'Niedziela')
)


class DayName(models.Model):
    name = models.CharField(max_length=32, choices=DayText, unique=True, default='Poniedziałek')
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    calories_in_100_grams = models.IntegerField(default=0)
    carbohydrates = models.DecimalField(max_digits=3, decimal_places=1)
    fats = models.DecimalField(max_digits=3, decimal_places=1)
    proteins = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientWeight')
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def calories(self):
        calories = 0
        recipe_ingredients = self.ingredients.all()
        for ingredient in recipe_ingredients:
            collection = IngredientWeight.objects.all()
            ingredient_calories = collection.filter(ingredient_id=ingredient.id).filter(recipe_id=self.id)[0]
            calories += ingredient_calories.ingredient_calories()
        return calories


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    def __str__(self):
        return self.name


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=64)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.PROTECT)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)


class IngredientWeight(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    weight_in_grams = models.IntegerField()

    def ingredient_calories(self):
        calories = (self.weight_in_grams * self.ingredient.calories_in_100_grams)/100
        return calories

