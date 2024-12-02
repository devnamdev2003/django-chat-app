from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        relation_key = username + "_" + user.username
        user_relation = UserRelation(
            user=user, friend=friend, accepted=accepted, relation_key=relation_key
        )
        user_relation.save()

        user_relation_revrse = UserRelation.objects.get(user=friend, friend=user)
        user_relation_revrse.accepted = True
        user_relation_revrse.relation_key = relation_key
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

