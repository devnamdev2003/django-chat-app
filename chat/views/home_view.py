from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation
from django.contrib import messages


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


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation
from django.contrib import messages
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


