from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserRelation, Messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from app1.serializers import MessageSerializer
from django.contrib import messages as django_messages  


@login_required(login_url="login")
def chat(request, username):
    try:
        usersen = request.user
        friend = User.objects.get(username=username)
        exists = UserRelation.objects.filter(
            user=request.user, friend=friend, accepted=True
        ).exists()

        if not exists:
            django_messages.error(
                request, "You are not able to chat with this user."
            )  # Use the renamed variable here
            return redirect("home")
    except User.DoesNotExist:
        return redirect("home")

    messages = Messages.objects.filter(
        sender_name=usersen, receiver_name=friend
    ) | Messages.objects.filter(sender_name=friend, receiver_name=usersen)
    if request.method == "GET":
        return render(
            request,
            "chat.html",
            {
                "messages": messages,
                "curr_user": usersen,
                "friend": friend,
            },
        )


@login_required(login_url="login")
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == "GET":
        messages = Messages.objects.filter(
            sender_name=sender, receiver_name=receiver, seen=False
        )
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required(login_url="login")
def delete_friend(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        try:
            print("starts")
            exists = UserRelation.objects.filter(user=user, friend=friend).exists()
            print("sts")
            if exists:
                pass
            else:
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER", reverse("home"))
                )
            user_relation = UserRelation.objects.get(user=user, friend=friend)
            user_relation.delete()

            user_relation_reverse = UserRelation.objects.get(user=friend, friend=user)
            user_relation_reverse.delete()
            messages.success(request, "Friend deleted successfully.")

        except UserRelation.DoesNotExist:
            messages.success(request, "Request deleted successfully.")
            pass
        return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="login")
def accept_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = True

        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()

        user_relation_revrse = UserRelation.objects.get(user=friend, friend=user)
        user_relation_revrse.accepted = True
        user_relation_revrse.save()
        messages.success(request, "Friend Added successfully.")

        return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="login")
def add_friend(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = False
        print("starts")
        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            print("star")
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()
        messages.success(request, "Request sended successfully.")

        return redirect("home")
    else:
        return redirect("home")


@login_required(login_url="login")
def search(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        if query:
            users = User.objects.filter(username__icontains=query)
            if users:
                return render(
                    request,
                    "search.html",
                    {"query": query, "users": users, "user": request.user.username},
                )
            else:
                not_found_message = f'No users found for "{query}"'
                return render(
                    request,
                    "search.html",
                    {
                        "query": query,
                        "not_found_message": not_found_message,
                    },
                )

    return render(request, "search.html", {"user": request.user.username})


@login_required(login_url="login")
def userprofile(request, username):
    if username == request.user.username:
        return redirect("/")
    friend_dict = {}
    request_dict = {}
    friend_dict["accepted"] = False
    request_dict["accepted"] = False
    friend_dict["name"] = ""
    send_request = False
    not_accepted = False
    me_not_accepted = False
    is_friend = False
    try:
        user = User.objects.get(username=username)
        friends_data = UserRelation.objects.all()
        for obj in friends_data:
            if obj.user.username == request.user.username:
                if obj.friend.username == username:
                    friend_dict = {
                        "name": obj.friend.username,
                        "accepted": obj.accepted,
                    }
        for obj in friends_data:
            if obj.friend.username == request.user.username:
                if obj.user.username == username:
                    if obj.accepted:
                        me_not_accepted = False
                    else:
                        me_not_accepted = True

    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return render(request, "friend.html")

    if friend_dict["name"] == "":
        if me_not_accepted == True:
            print("me not accepted")
        else:
            print("not a friend")
            send_request = True

    elif friend_dict["accepted"] == False:
        print("not_accepted")
        not_accepted = True

    else:
        print("friend")
        is_friend = True
    print("send_request = ", send_request)
    print("not_accepted = ", not_accepted)
    print("me_not_accepted = ", me_not_accepted)
    print("is_friend = ", is_friend)
    # You can now access user details, such as username, email, etc.
    user_details = {
        "username": user.username,
        "email": user.email,
        "send_request": send_request,
        "not_accepted": not_accepted,
        "is_friend": is_friend,
        "me_not_accepted": me_not_accepted,
    }

    return render(request, "friend.html", {"user_details": user_details})


@login_required(login_url="login")
def HomePage(request):
    friends_data = UserRelation.objects.all()
    friends_list = []
    for obj in friends_data:
        if obj.user.username == request.user.username:
            friend_dict = {"username": obj.friend.username, "accepted": obj.accepted}
            friends_list.append(friend_dict)

    request_list = []
    for obj in friends_data:
        if obj.friend.username == request.user.username:
            if not obj.accepted:
                request_dict = {"username": obj.user.username}
                request_list.append(request_dict)

    data = {
        "email": request.user.email,
        "username": request.user.username,
        "friends": friends_list,
        "requests": request_list,
    }
    return render(
        request,
        "home.html",
        {
            "data": data,
        },
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
            # print(request.user.id)
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
    email = ""
    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("pass")
        try:
            curr_user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = "Email not found. Please check your Email."
            return render(
                request, "login.html", {"error_message": error_message, "email": email}
            )

        user = authenticate(request, username=curr_user.username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            if User.objects.filter(username=curr_user.username).exists():
                error_message = "Incorrect password. Please try again."
            else:
                error_message = "Email not found. Please check your email."
    return render(
        request, "login.html", {"error_message": error_message, "email": email}
    )


def LogoutPage(request):
    logout(request)
    return redirect("login")
