from tasks.email import send_welcome_email
from tasks.forms import TaskingForm, UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request,'index.html')



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


def addTask(request):
    form = TaskingForm()

    if request.method == 'POST':
        form = TaskingForm(request.POST)

        if form.is_valid():
            form.save()

            # send_welcome_email(form.cleaned_data['username'], form.cleaned_data['email'])

            messages.success(request, 'Task added successfully')

            return redirect('home')

    return render(request,'taskform.html',{'form':form})
