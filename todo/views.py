from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDo_Form
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signup_user(request):
    if(request.method=='GET'):
        return render(request, 'todo/signup_user.html', {'form':UserCreationForm()})
    else: #create a new user using post request
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form':UserCreationForm(), 'error':'That username is already taken. Please choose a new Username.'})
        else:
            return render(request, 'todo/signup_user.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

@login_required
def logout_user(request):
    if (request.method=='POST'):
        logout(request)
        return redirect('home')
    
def login_user(request):
    if(request.method=='GET'):
        return render(request, 'todo/login_user.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if (user is None):
            return render(request, 'todo/login_user.html', {'form':AuthenticationForm(), 'error':"Username and Password did not match"})
        else:
            login(request, user)
            return redirect('current_todos')

@login_required
def create_todos(request):
    if(request.method=='GET'):
        return render(request, 'todo/create_todos.html', {'form':ToDo_Form()})
    else:
        try:
            form = ToDo_Form(request.POST)
            new_todo = form.save(commit=False)#don't put in database just yet
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todos.html', {'form':ToDo_Form(), 'error':'Error occured in data passed'})

@login_required
def current_todos(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=True)#only show current user todos
    return render(request, 'todo/current_todos.html', {'todos': todos})

@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    if(request.method=='GET'):
        form = ToDo_Form(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form':form})
    else:
        try:
            form = ToDo_Form(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_todo.html', {'todo': todo, 'form':form, 'error':'Error occured in data passed'})

@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if(request.method=='POST'):
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current_todos')
    
@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if(request.method=='POST'):
        todo.delete()
        return redirect('current_todos')

@login_required    
def completed_todos(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')#only show completed user todos
    return render(request, 'todo/completed_todos.html', {'todos': todos})