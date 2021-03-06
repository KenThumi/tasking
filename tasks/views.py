from tasks.models import Task
from tasks.email import send_task_challenge_notification_email, send_tasking_notification_email, send_welcome_email
from tasks.forms import ChallengeForm, TaskingForm, UpdateTaskPhaseForm, UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Rest API
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import TaskSerializer


@login_required
def home(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user= request.user)


    filter_form = UpdateTaskPhaseForm()


    ctx = {'tasks':tasks, 'filter_form':filter_form}

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



@login_required
def search(request):

    if request.method=='POST':

        needle = request.POST['search']

        if request.user.is_superuser:
            tasks=Task.objects.filter(title__icontains=needle).all()
        else:
            tasks=Task.objects.filter(user= request.user,title__icontains=needle).all()

        ctx = {'tasks':tasks, 'search_results':f'Search Results ({tasks.count()})', 'filter_form':UpdateTaskPhaseForm()}

        return render(request, 'index.html',ctx)

    return redirect('home')


@login_required
def filterphase(request):
    filter_form = UpdateTaskPhaseForm()

    if request.method=='POST':

        form = UpdateTaskPhaseForm(request.POST)

        if form.is_valid():

            if request.user.is_superuser:
                tasks=Task.objects.filter(phase=form.cleaned_data['phase']).all()
            else:
                tasks=Task.objects.filter(user= request.user,phase=form.cleaned_data['phase']).all()

            ctx = {'tasks':tasks, 'search_results':f'Search Results ({tasks.count()})','filter_form':filter_form}

            return render(request, 'index.html',ctx)

    return redirect('home')


def addChallenge(request,id):
    form = ChallengeForm()


    if request.method=='POST':

        form = ChallengeForm(request.POST)

        if form.is_valid():
            task = Task.objects.get(pk=id)

            if request.user.is_superuser == False:
                challenge = form.save(commit=False)
                challenge.task= task
                challenge.save()

                send_task_challenge_notification_email(task)

                messages.success(request, 'Chellenge added successfully')

                return redirect('home')
            else:
                messages.warning(request, 'Permission Denied')

                return redirect('home')
    

    ctx = {'form':form}

    return render(request, 'challengeForm.html', ctx)


# REST API views
class TaskList(APIView):
    def get(self, request, format=None):
        all_tasks= Task.objects.all()
        serializers = TaskSerializer(all_tasks, many=True)
        return Response(serializers.data)
