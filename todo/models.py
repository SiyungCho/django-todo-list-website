from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)#doesn't have to put in description
    created = models.DateTimeField(auto_now_add=True)#auto adds time and date
    datecompleted = models.DateTimeField(null=True, blank=True)#don't set time yet
    important = models.BooleanField(default=False)#check off if task is important
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

