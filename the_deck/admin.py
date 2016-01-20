from django.contrib import admin

from the_deck.models import *

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
  # list_display = ["name"]
  search_fields = ["name"]

@admin.register(ChefInventory)
class ChefInventoryAdmin(admin.ModelAdmin):
    search_fields = ["query"]

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
  search_fields = ["name", "fqdn"]

@admin.register(SshUser)
class SshUserAdmin(admin.ModelAdmin):
  search_fields = ["username"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  search_fields = ["command", "host", "username"]

@admin.register(RemoteFile)
class RemoteFileAdmin(admin.ModelAdmin):
  search_fields = ["filename"]

@admin.register(TaskRunner)
class TaskRunnerAdmin(admin.ModelAdmin):
  search_fields = ["state"]

@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
  search_fields = ["command"]

