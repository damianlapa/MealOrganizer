from datetime import datetime
import random
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from MealOrganizer.models import Recipe, Plan, RecipePlan, DayName, Page, Ingredient, IngredientWeight


class RecipeSearch(View):
    def get(self, request):
        return render(request, 'search-recipe.html')

    def post(self, request):
        recipe_name = request.POST.get("title")
        recipes = Recipe.objects.all().filter(name__icontains=recipe_name)
        counter = recipes.count()
        paginator = Paginator(recipes, 10)

        page = int(request.GET.get("page", 1))
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        recipes = paginator.get_page(page)
        text = recipe_name
        return render(request, "app-recipes.html", locals(), {"page": (page - 1) * 10})


class ContactSlug(View):
    def get(self, request):

        try:
            page = Page.objects.get(title='contact')
            title = page.title
            description = page.description

            return render(request, 'slug.html', locals())

        except Page.DoesNotExist:
            return redirect('/#contact')


class AboutSlug(View):
    def get(self, request):

        try:
            page = Page.objects.get(title='about')
            title = page.title
            description = page.description

            return render(request, 'slug.html', locals())

        except Page.DoesNotExist:
            return redirect('/#about')


class MainPage(View):

    def get(self, request):
        recipes = Recipe.objects.all()
        recipes = list(recipes)
        random.shuffle(recipes)

        recipe1 = recipes[0]
        recipe2 = recipes[1]
        recipe3 = recipes[2]

        ctx = {'recipe1': recipe1, 'recipe2': recipe2, 'recipe3': recipe3}

        return render(request, "index.html", ctx)


class DashboardView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        plan_count = Plan.objects.count()
        recipe_count = Recipe.objects.count()

        last_plan = Plan.objects.all().order_by('created')[0]
        last_plan_meals = RecipePlan.objects.filter(plan_id=last_plan.id).order_by('order')
        days = DayName.objects.all()

        return render(request, "dashboard.html", locals())


# lista przepisów
class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipes, 10)

        page = int(request.GET.get("page", 1))
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {"recipes": recipes, "page": (page - 1) * 10})


# przepis o podanym id
class RecipeDetailsView(View):

    def get(self, request, rec_id):
        recipe = Recipe.objects.get(id=rec_id)
        ingredients = IngredientWeight.objects.all().filter(recipe_id=recipe.id)
        return render(request, "app-recipe-details.html", locals())

    def post(self, request, rec_id):
        recipe_id = request.POST.get("recipe_id")
        recipe = Recipe.objects.get(id=int(recipe_id))
        choice = request.POST.get("like")
        if choice:
            if choice == "Polub ten przepis":
                recipe.votes += 1
            elif choice == "Nie lubie przepisu":
                recipe.votes -= 1
        recipe.save()
        return redirect("/recipe/{}".format(recipe_id))


# dodanie nowego przepisu
class RecipeAddView(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)
        ingredients = request.POST.get("ingredients", None)
        preparation_time = request.POST.get("preparation_time", None)
        preparation_method = request.POST.get("preparation_method", None)

        if None in (name, description, ingredients, preparation_time, preparation_method):
            statement = "Brak wszystkich potrzebnych danych do stworzenia przepisu!"
            return render(request, "app-add-recipe.html", {'statement': statement})
        elif "" in (name, description, ingredients, preparation_time, preparation_method):
            if preparation_method == "":
                field = "SPOSÓB PRZYGOTOWANIA"
            if preparation_time == "":
                field = "Przygotowanie(minuty)"
            if ingredients == "":
                field = "SKŁADNIKI"
            if description == "":
                field = "Opis Przepisu"
            if name == "":
                field = "Nazwa Przepisu"
            statement = "Wypełnij poprawnie wszystkie pola. Pole {} nie może być puste!".format(field)
            return render(request, "app-add-recipe.html", {'statement': statement})
        else:
            Recipe.objects.create(name=name, description=description, ingredients=ingredients,
                                  preparation_time=preparation_time)
            return redirect("/recipe/list")


# modyfikowanie przepisu o podanym id
class RecipeModifyView(View):

    def get(self, request, rec_id):
        recipe_id = rec_id
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return render(request, 'app-edit-recipe.html', {"recipe": recipe})

    def post(self, request, rec_id):
        recipe_id = rec_id
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)
        ingredients = request.POST.get("ingredients", None)
        preparation_time = request.POST.get("preparation_time", None)
        preparation_method = request.POST.get("preparation_method", None)

        if None in (name, description, ingredients, preparation_time, preparation_method):
            statement = "Brak wszystkich potrzebnych danych do stworzenia przepisu!"
            return render(request, "app-add-recipe.html", {'statement': statement})
        elif "" in (name, description, ingredients, preparation_time, preparation_method):
            if preparation_method == "":
                field = "SPOSÓB PRZYGOTOWANIA"
            if preparation_time == "":
                field = "Przygotowanie(minuty)"
            if ingredients == "":
                field = "SKŁADNIKI"
            if description == "":
                field = "Opis Przepisu"
            if name == "":
                field = "Nazwa Przepisu"
            statement = "Wypełnij poprawnie wszystkie pola. Pole {} nie może być puste!".format(field)
            return render(request, "app-add-recipe.html", {'statement': statement})
        else:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.name = name
            recipe.preparation_time = preparation_time
            recipe.ingredients = ingredients
            recipe.description = description
            recipe.save()

        return redirect("/recipe/list")


# lista planów
class PlanListView(View):

    def get(self, request):
        plans = Plan.objects.all().order_by("name")
        paginator = Paginator(plans, 10)

        page = int(request.GET.get("page", 1))
        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)

        plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {"plans": plans, "page": (page - 1) * 10})


# dodanie nowego planu
class NewPlanView(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):

        planName = request.POST.get("planName", None)
        planDescription = request.POST.get("planDescription", None)

        if None in (planName, planDescription):
            statement = "Brak wszystkich potrzebnych danych do stworzenia planu!"
            return render(request, "app-add-schedules.html", locals())
        elif "" in (planName, planDescription):
            statement = "Nie wypelniono poprawnie wszystkich wymaganych pol"
            return render(request, "app-add-schedules.html", locals())
        else:
            try:
                plan = Plan.objects.create(name=planName, description=planDescription)
                statement = f"Stworzono plan {plan.name}"
            except:
                statement = f"Nie udalo sie stworzyc planu {plan.name}"
            return render(request, "app-add-schedules.html", locals())


# Dodanie przepisu do planu
class PlanAddRecipeView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        return render(request, 'app-schedules-meal-recipe.html', locals())

    # dla zadania 9.2 oblsuga posta
    def post(self, request):
        plan_name = request.POST.get('plan_name', None)
        recipe_name = request.POST.get('recipe', None)
        meal_name = request.POST.get("meal_name", None)
        meal_nr = request.POST.get("order", None)
        day = request.POST.get("day", None)

        if None in (plan_name, recipe_name, meal_name, meal_nr, day):
            statement = "Potrzeba wszystkich danych do utworzenia posiłku!"
            return render(request, 'app-schedules-meal-recipe.html', locals())

        plan = Plan.objects.get(name=plan_name)
        recipe = Recipe.objects.get(name=recipe_name)
        order = int(meal_nr)
        day = DayName.objects.get(name=day)

        RecipePlan.objects.create(meal_name=meal_name, plan=plan, recipe=recipe, order=order, day_name=day)

        return redirect("/plan/{}/".format(plan.id))


# szczegóły planu o podanym id
class PlanDetailsView(View):

    def get(self, request, plan_id):
        plan = Plan.objects.get(id=plan_id)
        days = DayName.objects.all()
        plan_meals = RecipePlan.objects.filter(plan_id=plan_id).order_by("order")
        return render(request, "app-details-schedules.html", locals())

    def post(self, request, plan_id):
        recipe_plan_id = request.POST.get('meal_id', None)
        delete = request.POST.get('delete', None)
        if delete:
            recipe_plan = RecipePlan.objects.get(id=recipe_plan_id)
            recipe_plan.delete()

        plan = Plan.objects.get(id=plan_id)
        days = DayName.objects.all()
        plan_meals = RecipePlan.objects.filter(plan_id=plan_id).order_by("order")
        return render(request, "app-details-schedules.html", locals())


# modyfikowanie planu o podanym id
class PlanModifyView(View):

    def get(self, request, plan_id):
        plan = get_object_or_404(Plan, id=plan_id)
        return render(request, 'app-edit-schedules.html', {"plan": plan})

    def post(self, request, plan_id):
        name = request.POST.get("name")
        description = request.POST.get("description")

        plan = Plan.objects.get(pk=plan_id)
        plan.name = name
        plan.description = description
        plan.save()

        statement = "{} dodany!".format(name)

        return render(request, 'app-edit-schedules.html', locals())


class IngredientsList(View):

    def get(self, request):
        ingredients = Ingredient.objects.all().order_by("name")
        paginator = Paginator(ingredients, 10)

        page = int(request.GET.get("page", 1))
        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)

        plans = paginator.get_page(page)
        return render(request, "ingredients-list.html", {"ingredients": ingredients, "page": (page - 1) * 10})
