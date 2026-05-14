from django import forms

from .models import Dish, DishType, Cook, Task

class DishForm(forms.ModelForm):
    class Meta:
        model=Dish
        fields = "__all__"

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "deadline", "cook"]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            )
        }



