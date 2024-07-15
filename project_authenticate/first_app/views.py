from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash

def home(request):
    return render(request,'base.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,"Account created succesfully!")
            form.save()
    else:
        form = RegisterForm()
    return render(request,'signup.html',{'form':form })

def user_login(request):
    if request.method == "POST":
        form= AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            messages.success(request,"Logged in succesfully!")
            name = form.cleaned_data['username']
            userpass = form.cleaned_data['password']
            user = authenticate(username = name ,password = userpass)
            if user is not None:
                login(request,user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form })
    
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'user':request.user})
    else:
        return redirect('login')

def user_logout(request):
    messages.success(request,"Logged Out succesfully!")
    logout(request)
    return redirect('home')

def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                update_session_auth_hash(request,form.cleaned_data['user'])
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'passchange.html',{'form':form})
    else:
        return redirect('home')

def pass_change2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user,data=request.POST)
            if form.is_valid():
                update_session_auth_hash(request,form.cleaned_data['user'])
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'passchange.html',{'form':form})
    else:
        return redirect('home')
