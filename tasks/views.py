from tasks.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request,'index.html')



def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            # send_welcome_email(form.cleaned_data['username'], form.cleaned_data['email'])

            messages.success(request, 'Successful Registration. Welcome email sent to your email.')

            return redirect('login')

    return render(request,'registration/register.html',{'form':form})
