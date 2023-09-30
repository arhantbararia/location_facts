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

def LoginView():
    pass

def LogoutView():
    pass