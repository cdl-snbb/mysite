from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserTable)
class UserTableAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    ordering = ["id"]

# admin.site.register(UserTable, UserTableAdmin)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', "text", 'comment_time')