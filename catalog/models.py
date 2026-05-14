from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType,
                                  on_delete=models.CASCADE,
                                  related_name="dishes")
    cooks = models.ManyToManyField(Cook)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.description}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    cook = models.ForeignKey(Cook,
                                  on_delete=models.CASCADE,
                                  related_name="tasks")
    @property
    def is_overdue(self):
        return self.deadline < timezone.now()