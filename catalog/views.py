from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from .models import Dish, Cook, DishType
from .forms import DishForm

class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "catalog/dish_list.html"

class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "catalog/cook_list.html"

class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "catalog/dish_type_list.html"

class DishDetailView(generic.DetailView):
    model = Dish
    context_object_name = "dish-detail"
    template_name = "catalog/dish-detail.html"

class CookDetailView(generic.DetailView):
    model = Cook
    context_object_name = "cook-detail"
    template_name = "catalog/cook-detail.html"

class DishTypeDetailView(generic.DetailView):
    model = DishType
    context_object_name = "dish_type-detail"
    template_name = "catalog/dish_type-detail.html"

class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("dish-list")
    template_name = "catalog/dish_form.html"

class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("dish-list")
    template_name = "catalog/dish_confirm_delete.html"

class DishCreateView(generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("dish-list")
    template_name = "catalog/dish_form.html"


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")