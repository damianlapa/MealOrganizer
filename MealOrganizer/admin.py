from django.contrib import admin

from .models import *

admin.site.register(Recipe)
admin.site.register(RecipePlan)
admin.site.register(Plan)
admin.site.register(DayName)
