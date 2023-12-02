from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


def user_dir_path(instance, filename):
    return "uploads/avatars/{0}/{1}".format(instance.username, filename)


def task_dir_path(instance, filename):
    return "uploads/tasks/{0}/{1}".format(instance.name, filename)


def project_dir_path(instance, filename):
    return "uploads/projects/{0}/{1}".format(instance.name, filename)


def comment_attach_dir_path(instance, filename):
    return "uploads/tasks/attachments/{1}".format(filename)


class Manager(AbstractUser):
    # Manager DB Models

    avatar = models.ImageField(
        upload_to=user_dir_path, default="static/images/users/user-1.jpg"
    )

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Project(models.Model):
    class ProjectStatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        DEACTIVE = "deactive", "Deactive"

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created_by = models.ForeignKey(
        Manager, on_delete=models.CASCADE, related_name="created_by"
    )
    managers = models.ManyToManyField(Manager)

    status = models.CharField(
        max_length=16,
        choices=ProjectStatusChoices.choices,
        default=ProjectStatusChoices.DEACTIVE,
    )

    avatar = models.ImageField(
        upload_to=task_dir_path, default="static/images/all-img/card-6.png"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class TasksStatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    avatar = models.ImageField(
        upload_to=task_dir_path, default="static/images/all-img/card-7.png"
    )
    created_by = models.ForeignKey(Manager, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=16,
        choices=TasksStatusChoices.choices,
        default=TasksStatusChoices.PENDING,
    )

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Manager, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    attachment = models.FileField(upload_to=comment_attach_dir_path, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.text
