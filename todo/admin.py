from django.contrib import admin
from .models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(ToDo, ToDoAdmin)