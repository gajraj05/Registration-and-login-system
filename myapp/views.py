from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user already exists
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'User already exists!')
            return redirect('/register/')
        
        # Create a new user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            # password=password  # Password should be hashed/ more secure
        )
        
        user.set_password(password)
        user.save()

        messages.success(request, 'User registered successfully!')
        return redirect('index')

    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User does not exist!')
            return redirect('/register/')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Username or Password!')
            return redirect('/login/')
        else:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('index')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/login/')