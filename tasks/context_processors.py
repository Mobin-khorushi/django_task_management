from django.contrib.auth import get_user
from itertools import chain


def project_names_processor(request):
    user = get_user(request)
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
        return {"project_names": project_names}
    return {"project_names": []}
