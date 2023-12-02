from django.contrib import admin

from .models import Manager, Project, Task, Comment

from django.contrib.auth.admin import UserAdmin

# Register your models here.


class ManagerAdmin(UserAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "username",
        "password",
        "avatar",
        "created_at",
        "updated_at",
    ]


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "created_by",
        "status",
        "avatar",
        "created_at",
        "updated_at",
    ]


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "name",
        "description",
        "avatar",
        "created_by",
        "status",
        "created_at",
        "updated_at",
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "text",
        "task",
        "created_by",
        "edited",
        "attachment",
        "created_at",
        "updated_at",
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
