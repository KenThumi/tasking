from tasks.models import Task
from tasks.email import send_tasking_notification_email, send_welcome_email
from tasks.forms import TaskingForm, UpdateTaskPhaseForm, UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required
def home(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user= request.user)


    ctx = {'tasks':tasks}

    return render(request,'index.html',ctx)



def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            send_welcome_email(form.cleaned_data['username'], form.cleaned_data['email'])

            messages.success(request, 'Successful Registration. Welcome email sent to your email.')

            return redirect('login')

    return render(request,'registration/register.html',{'form':form})

@login_required
def addTask(request):
    form = TaskingForm()

    if request.method == 'POST':
        form = TaskingForm(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.filter(username= form.cleaned_data['user']).first()

            send_tasking_notification_email(user)

            messages.success(request, 'Task added successfully')

            return redirect('home')

    return render(request,'taskform.html',{'form':form})

@login_required
def updatePhase(request, id):
    task = Task.objects.get(pk=id)

    if request.method == 'POST':
        form = UpdateTaskPhaseForm(request.POST)

        if form.is_valid():
            task.phase = form.cleaned_data['phase']

            task.save()

            messages.success(request, 'Task phase updated successfully')

            return redirect('home')


    form = UpdateTaskPhaseForm()


    if task != None:
        form = UpdateTaskPhaseForm(instance=task)
   

    return render(request,'updatephaseform.html',{'form':form})


@login_required
def updateTask(request,id):
    task = Task.objects.get(pk=id)

    if request.method == 'POST':
        form = TaskingForm(request.POST)

        if form.is_valid():
            Task.objects.filter(id=id).update(title=form.cleaned_data['title'], description=form.cleaned_data['description'], user=form.cleaned_data['user'])

            user = User.objects.filter(username= form.cleaned_data['user']).first()

            send_tasking_notification_email(user)

            messages.success(request, 'Task updated successfully')

            return redirect('home')

    
    form = TaskingForm(instance=task)

    return render(request,'taskform.html',{'form':form})


@login_required
def deleteTask(request,id):
    task = Task.objects.get(pk=id)

    task.delete()

    messages.success(request, 'Task deleted successfully')

    return redirect('home')
