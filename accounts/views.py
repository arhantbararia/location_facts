from django.shortcuts import render, redirect

from django.contrib.auth import authenticate , login , logout
from django.contrib import messages

from .forms import SignUpForm 


# Create your views here.



def RegisterView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if(form.is_valid()):
            form.save()
        
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username , password = password )
            login(request, user)
            messages.success(request, "Registered!")
            return redirect('location_facts')
    else:
        form = SignUpForm() 
        return render(request , "accounts/register.html" , {'form':form})
    
    return render(request , "accounts/register.html" , {'form':form})

def LoginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username= username , password = password)

        if user is not None:
            login(request, user)
            messages.success(request ,f"Logged in! Welcome {user}")
            return redirect('location_facts')
        else:
            messages.success(request , "Login Failed!")
            redirect('login')
    
    return render(request , 'accounts/login.html')


def LogoutView(request):
    logout(request)
    messages.success(request , "Logged Out!")
    return redirect('location_facts')
