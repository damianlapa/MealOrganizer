"""MealManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mealorganizer.views import RecipeAddView, RecipeDetailsView, RecipeListView, RecipeModifyView
from mealorganizer.views import PlanListView, PlanAddRecipeView, RecipeSearch, IngredientsList, AddIngredient
from mealorganizer.views import MainPage, DashboardView, NewPlanView, PlanDetailsView, ContactSlug, AboutSlug, \
    PlanModifyView, IngredientDetails

urlpatterns = [
    path('ingredient/list', IngredientsList.as_view(), name='ingredient-list'),
    path('ingredient/add', AddIngredient.as_view(), name='add-ingredient'),
    path('ingredient/<int:ingredient_id>/', IngredientDetails.as_view(), name='ingredient-details'),
    path('search', RecipeSearch.as_view()),
    path('contact', ContactSlug.as_view()),
    path('about', AboutSlug.as_view()),
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main-page'),
    path('main/', DashboardView.as_view()),
    path('recipe/<int:rec_id>/', RecipeDetailsView.as_view()),
    path('recipe/list/', RecipeListView.as_view()),
    path('recipe/add/', RecipeAddView.as_view(), name='recipe-add'),
    path('recipe/modify/<int:rec_id>/', RecipeModifyView.as_view()),
    path('plan/list/', PlanListView.as_view()),
    path('plan/add/', NewPlanView.as_view()),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
    path('plan/add/', NewPlanView.as_view()),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
    path('plan/<int:plan_id>/', PlanDetailsView.as_view()),
    path('plan/modify/<int:plan_id>', PlanModifyView.as_view()),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
]
