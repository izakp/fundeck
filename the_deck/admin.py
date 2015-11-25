from django.contrib import admin

from the_deck.models import *

@admin.register(HostSet)
class HostSetAdmin(admin.ModelAdmin):
  search_fields = ["name"]

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
  search_fields = ["name", "query"]

@admin.register(StaticHost)
class StaticHostAdmin(admin.ModelAdmin):
  search_fields = ["name", "fqdn"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  search_fields = ["name", "run_command"]

@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
  search_fields = ["level", "log"]

@admin.register(TaskRunResult)
class TaskRunResultAdmin(admin.ModelAdmin):
  search_fields = ["result"]

@admin.register(TaskRunner)
class TaskRunnerAdmin(admin.ModelAdmin):
  search_fields = ["state"]

@admin.register(TaskSet)
class TaskSetAdmin(admin.ModelAdmin):
  search_fields = ["name"]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
  search_fields = ["username"]

