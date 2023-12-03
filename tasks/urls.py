from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_user, name="login_user"),
    path("logout", views.logout_user, name="logout_user"),
    path("register", views.register_user, name="register_user"),
    # Project Paths
    path("projects/create", views.project_add, name="project_add"),
    path("projects/list", views.project_list, name="project_list"),
    path("projects/view/<int:id>", views.project_view, name="project_view"),
    path("projects/assign/<int:id>", views.project_assign, name="project_assign"),
    path(
        "projects/unassign/<int:project_id>/<int:user_id>",
        views.project_unassign,
        name="project_unassign",
    ),
    path(
        "projects/update/<int:id>",
        views.project_update,
        name="project_update",
    ),
    path(
        "projects/delete/<int:id>",
        views.project_delete,
        name="project_delete",
    ),
    path("tasks/<int:project_id>", views.tasks_list, name="tasks_list"),
    path("tasks/create/<int:project_id>", views.tasks_create, name="tasks_create"),
    path("tasks/<int:project_id>/<int:task_id>", views.tasks_view, name="tasks_view"),
    path(
        "tasks/status/<int:task_id>",
        views.tasks_status_change,
        name="tasks_status_change",
    ),
    path(
        "tasks/update/<int:task_id>",
        views.tasks_update,
        name="tasks_update",
    ),
    path(
        "tasks/delete/<int:task_id>",
        views.tasks_delete,
        name="tasks_delete",
    ),
    path("comments/view/<int:task_id>", views.comments_view, name="comments_view"),
]
