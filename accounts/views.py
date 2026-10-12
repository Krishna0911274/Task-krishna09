from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "accounts/home.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration successful!")
            return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            if user.groups.filter(name="MRO").exists():
                return redirect("mro:dashboard")
            elif user.groups.filter(name="TM").exists():
                return redirect("tm:dashboard")
            elif user.groups.filter(name="Engineer").exists():
                return redirect("engineer:dashboard")
            elif user.groups.filter(name="Head").exists():
                return redirect("head:dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")
