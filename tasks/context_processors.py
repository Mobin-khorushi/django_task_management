from django.contrib.auth import get_user
from django.contrib.auth.models import User
from itertools import chain
from .models import Manager


def project_names_processor(request):
    try:
        user = get_user(request)
        users = Manager.objects.values_list("username", flat=True)
        if user:
            projects = user.project_set.all()
            user_made_projects = user.created_by.all()
            result_list = list(chain(user_made_projects, projects))
            project_names = []

            for project in result_list:
                tasks_names = []
                tasks = project.task_set.all()
                for task in tasks:
                    tasks_names.append({"id": task.id, "name": task.name})
                project_names.append(
                    {"id": project.id, "name": project.name, "tasks": tasks_names}
                )
            return {"project_names": project_names, "users_names": users}
    except:
        pass
    return {"project_names": [], "users_names": []}
