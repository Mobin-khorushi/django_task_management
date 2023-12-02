from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Manager, Project
from django.shortcuts import redirect
from .forms import ProjectsForm

import re
from itertools import chain


def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email):
        return True

    return False


# Create your views here.
@login_required()
def home(request):
    return render(request, "views/dashboard/home.html", {})


@login_required()
def project_list(request):
    user = get_user(request)
    user_projects = user.project_set.all()
    user_made_projects = user.created_by.all()
    result_list = list(chain(user_made_projects, user_projects))

    return render(
        request,
        "views/dashboard/projects/list.html",
        {"projects": result_list},
    )


@login_required()
def project_update(request, id):
    if request.method == "POST":
        project = Project.objects.filter(id=id).first()
        if project:
            user = get_user(request)
            if project.created_by.id == user.id:
                formData = ProjectsForm(request.POST, request.FILES)
                if formData.is_valid():
                    if formData.cleaned_data["cover_image"]:
                        project.avatar = formData.cleaned_data["cover_image"]

                    project.name = formData.cleaned_data["name"]
                    project.description = formData.cleaned_data["description"]
                    project.status = formData.cleaned_data["status_select"]

                    project.save()
                    return redirect("project_list")

    return redirect("project_list")


@login_required()
def project_delete(request, id):
    project = Project.objects.filter(id=id).first()
    if project:
        user = get_user(request)
        if project.created_by.id == user.id:
            project.delete()

    return redirect("project_list")


@login_required()
def project_add(request):
    if request.method == "POST":
        try:
            formData = ProjectsForm(request.POST, request.FILES)
            if formData.is_valid():
                new_project = Project(
                    name=formData.cleaned_data["name"],
                    description=formData.cleaned_data["description"],
                    status=formData.cleaned_data["status_select"],
                )
                if formData.cleaned_data["cover_image"]:
                    new_project.avatar = formData.cleaned_data["cover_image"]

                new_project.created_by = get_user(request)
                new_project.save()
                return redirect("home")
        except Exception as e:
            print("ERROR")
            print(e)
            return render(
                request,
                "views/dashboard/projects/create.html",
                {"errors": "Creating Project Failed"},
            )

    return render(request, "views/dashboard/projects/create.html", {})


def login_user(request):
    if request.method == "POST":
        login_input = request.POST.get("username")
        password_input = request.POST.get("password")
        if not (login_input and login_input.strip()) or not (
            password_input and password_input.strip()
        ):
            return render(
                request, "views/auth/login.html", {"errors": "Login Failed !"}
            )
        login_username = login_input
        if "@" in login_input:
            user = Manager.objects.filter(email=login_input).first()
            login_username = user.username
        user = authenticate(request, username=login_username, password=password_input)
        try:
            login(request, user)
            return redirect("home")
        except:
            return render(
                request, "views/auth/login.html", {"errors": "Login Failed !"}
            )
    return render(request, "views/auth/login.html", {})


def register_user(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        if not (username_input and username_input.strip()):
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Username cannot be empty"},
            )
        if len(username_input) < 3:
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Username cannot be less than 3 chars"},
            )
        if Manager.objects.filter(username=username_input).exists():
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Username already exists"},
            )
        email_input = request.POST.get("email")
        if not (email_input and email_input.strip()):
            return render(
                request, "views/auth/register.html", {"errors": "Email cannot be empty"}
            )
        if not validate_email(email_input):
            return render(
                request, "views/auth/register.html", {"errors": "Email wrong format"}
            )
        if Manager.objects.filter(email=email_input).exists():
            return render(
                request,
                "views/auth/register.html",
                {"errors": "email already exists"},
            )
        first_name_input = request.POST.get("first_name")
        if not (first_name_input and first_name_input.strip()):
            return render(
                request,
                "views/auth/register.html",
                {"errors": "First name cannot be empty"},
            )
        last_name_input = request.POST.get("last_name")
        if not (last_name_input and last_name_input.strip()):
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Last name cannot be empty"},
            )
        password_input = request.POST.get("password")
        if not (password_input and password_input.strip()):
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Password cannot be empty"},
            )
        if len(password_input) < 6:
            return render(
                request,
                "views/auth/register.html",
                {"errors": "Password cannot be less than 6 chars"},
            )

        user = Manager(
            username=username_input,
            email=email_input,
            first_name=first_name_input,
            last_name=last_name_input,
        )
        user.save()
        user.set_password(password_input)
        user.save()

        user_auth = authenticate(
            request, username=username_input, password=password_input
        )
        try:
            login(request, user_auth)
            return redirect("home")
        except:
            return render(
                request, "views/auth/login.html", {"errors": "Login Failed !"}
            )
    return render(request, "views/auth/register.html", {})


@login_required()
def logout_user(request):
    logout(request)
    return redirect("login_user")
