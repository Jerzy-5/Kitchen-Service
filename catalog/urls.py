from django.urls import path

from .views import (DishListView,
                    CookListView,
                    DishTypeListView,
                    DishDetailView,
                    CookDetailView,
                    DishTypeDetailView,
                    DishUpdateView,
                    DishDeleteView,
                    DishCreateView,
                    TaskCreateView,
                    TaskListView,
                    complete_task,
                    delete_task)

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("dish_types/", DishTypeListView.as_view(), name="dish_type-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("dish_types/<int:pk>/", DishTypeDetailView.as_view(), name="dish_type-detail"),
    path("dishes/<int:pk>/update", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/create", DishCreateView.as_view(), name="dish-create"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
path("tasks/", TaskListView.as_view(), name="task-list"),
path("tasks/<int:pk>/complete/", complete_task, name="task-complete"),
path("tasks/<int:pk>/delete/", delete_task, name="task-delete")

]