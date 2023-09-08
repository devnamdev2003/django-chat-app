from django.shortcuts import render
# from .models import UserRelation
from django.contrib.auth.decorators import login_required


# @login_required(login_url="login")
# def list_friends(request):
#     # Query for all data of UserRelation
#     friends_data = UserRelation.objects.all()

#     return render(request, "home.html", {"friends_data": friends_data})
