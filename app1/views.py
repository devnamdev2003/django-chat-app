from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def HomePage(request):
    data = {
        "email": request.user.email,
        "username": request.user.username,
    }

    return render(
        request,
        "home.html",
        {"data": data},
    )


@login_required(login_url="login")
def EditProfile(request):
    success_message = None
    error_message = None

    if request.method == "POST":
        new_email = request.POST.get("email")
        new_username = request.POST.get("username")

        # Check if the new username is already taken
        if (
            new_username != request.user.username
            and User.objects.filter(username=new_username).exists()
        ):
            error_message = "Username already exists. Please choose a different one."
        elif (
            new_email != request.user.email
            and User.objects.filter(email=new_email).exists()
        ):
            error_message = "Email address already associated with another account. Please choose a different one."
        else:
            # Update email and username
            request.user.email = new_email
            request.user.username = new_username
            request.user.save()
            success_message = "Profile updated successfully."

    # Pre-fill the form with the user's existing data
    initial_data = {
        "email": request.user.email,
        "username": request.user.username,
    }

    return render(
        request,
        "edit.html",
        {
            "initial_data": initial_data,
            "success_message": success_message,
            "error_message": error_message,
        },
    )


def SignupPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    error_message = ""  # Initialize error_message as None

    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        data = {
            "username": uname,
            "useremail": email,
        }

        # Check if a user with the same email or username already exists
        if User.objects.filter(username=uname).exists():
            error_message = "A user with the same username already exists."
            return render(
                request,
                "signup.html",
                {"error_message": error_message, "userdata": data},
            )

        elif User.objects.filter(email=email).exists():
            error_message = "A user with the same email already exists."
            return render(
                request,
                "signup.html",
                {"error_message": error_message, "userdata": data},
            )

        else:
            # Create the user
            user = User.objects.create_user(username=uname, email=email, password=pass1)
            user.save()
            # Log the user in after registration
            login(request, user)
            return redirect("home")

    return render(request, "signup.html", {"error_message": error_message})


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Check if the username exists
            if User.objects.filter(username=username).exists():
                error_message = "Incorrect password. Please try again."
            else:
                error_message = "Username not found. Please check your username."
    return render(request, "login.html", {"error_message": error_message})


def LogoutPage(request):
    logout(request)
    return redirect("login")
