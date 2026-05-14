import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import DishForm, TaskForm
from .models import Dish, Cook, Task, DishType

class DishModelTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Soup")
        self.dish = Dish.objects.create(
            name="Tomato Soup",
            price=12.50,
            dish_type=self.dish_type
        )

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "Tomato Soup")

    def test_dish_type(self):
        self.assertEqual(str(self.dish_type), "Soup")

    def test_dish_price_value(self):
        self.assertEqual(self.dish.price, 12.50)

class TaskModelTests(TestCase):

    def setUp(self):
        self.chef = Cook.objects.create(username="Gordon")
        self.overdue_task = Task.objects.create(title="Wash the dishes",
                                                deadline=timezone.now() - datetime.timedelta(days=1),
                                                cook=self.chef)
        self.on_time_task = Task.objects.create(title="Wash the dishes",
                                                deadline=timezone.now() + datetime.timedelta(days=1),
                                                cook=self.chef)

    def test_task_is_overdue(self):
        self.assertEqual(self.overdue_task.is_overdue, True)

    def test_task_is_not_overdue(self):
        self.assertEqual(self.on_time_task.is_overdue, False)

    def test_new_cook_years_of_experience(self):
        self.assertEqual(self.chef.years_of_experience, 0)


class CatalogViewTest(TestCase):
    def setUp(self):
        self.type = DishType.objects.create(name="Italian")
        self.cook = Cook.objects.create(username="Mario", years_of_experience=5)
        self.dish = Dish.objects.create(
            name="Pizza",
            price=30.00,
            dish_type=self.type
        )

    def test_dish_list_view(self):
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/dish_list.html")
        self.assertContains(response, "Pizza")

    def test_dish_detail_view(self):
        response = self.client.get(reverse("dish-detail", kwargs={"pk": self.dish.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertEqual(response.context["dish-detail"].price, 30.00)


class TaskActionViewTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create(username="Luigi")
        self.task = Task.objects.create(
            title="Clean Oven",
            deadline=timezone.now(),
            cook=self.cook,
            completed=False
        )

    def test_complete_task_view(self):
        url = reverse("task-complete", kwargs={"pk": self.task.pk})
        response = self.client.get(url)

        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        self.assertRedirects(response, reverse("task-list"))

    def test_delete_task_view(self):
        url = reverse("task-delete", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(Task.objects.count(), 1)

        response = self.client.post(url)
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse("task-list"))


class DishCreateViewTest(TestCase):

    def setUp(self):
        self.type = DishType.objects.create(name="Soup")
        self.cook = Cook.objects.create(username="TestChef")

    def test_create_dish_via_post(self):
        form_data = {
            "name": "Tomato Soup",
            "description": "Tasty",
            "price": "15.00",
            "dish_type": self.type.id,
            "cooks": [self.cook.id]
        }
        response = self.client.post(reverse("dish-create"), data=form_data)

        self.assertRedirects(response, reverse("dish-list"))
        self.assertTrue(Dish.objects.filter(name="Tomato Soup").exists())

class DishFormTest(TestCase):

    def setUp(self):
        self.type = DishType.objects.create(name="Main Course")
        self.cook = Cook.objects.create(username="testcook")

    def test_dish_form_valid(self):
        form_data = {
            "name": "Pasta Carbonara",
            "description": "Classic italian pasta",
            "price": 20.00,
            "dish_type": self.type.id,
            "cooks": [self.cook.id]
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid_price(self):
        form_data = {
            "name": "Pasta",
            "price": "not-a-number",
            "dish_type": self.type.id,
            "cooks": [self.cook.id]
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

class TaskFormTest(TestCase):

    def setUp(self):
        self.cook = Cook.objects.create(username="ChefJacek")

    def test_task_form_valid(self):
        form_data = {
            "title": "Clean fridge",
            "deadline": "2026-05-20T12:00",
            "cook": self.cook.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_missing_field(self):
        form_data = {
            "title": "",
            "deadline": "2026-05-20T12:00",
            "cook": self.cook.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_task_form_invalid_deadline_format(self):
        form_data = {
            "title": "Task",
            "deadline": "13.05.2026",
            "cook": self.cook.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
