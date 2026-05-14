from django.contrib import admin
from .models import Dish, Cook, DishType, Task

admin.site.register(DishType)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "dish_type")
    list_filter = ("price", "dish_type")
    search_fields = ("name", "description")


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    list_display = ("username", "years_of_experience")
    list_filter = ["years_of_experience"]
    search_fields = ["username"]

@admin.register(Task)
class CookAdmin(admin.ModelAdmin):
    list_display = ("title", "deadline", "cook")
    list_filter = ["deadline"]
    search_fields = ["title"]