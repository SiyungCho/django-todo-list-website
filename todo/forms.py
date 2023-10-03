from django.forms import ModelForm
from .models import ToDo

class ToDo_Form(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'important']