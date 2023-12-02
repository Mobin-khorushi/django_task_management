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
]
