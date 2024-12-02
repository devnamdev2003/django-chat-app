from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import UserRelation, Messages
from django.http.response import JsonResponse
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
            django_messages.error(request, "You are not able to chat with this user.")
            return redirect("home")  # Ensure we return a response here

    except User.DoesNotExist:
        return redirect("home")  # Ensure we return a response here

    # Get the messages
    messages = Messages.objects.filter(
        sender_name=usersen, receiver_name=friend
    ) | Messages.objects.filter(sender_name=friend, receiver_name=usersen)

    if request.method == "GET":
        try:
            # Ensure UserRelation exists
            relation = UserRelation.objects.get(
                user=request.user, friend=friend, accepted=True
            )
            return render(
                request,
                "chat.html",
                {
                    "relation_key": relation.relation_key,
                    "messages": messages,
                    "curr_user": usersen,
                    "friend": friend,
                },
            )
        except UserRelation.DoesNotExist:
            # If no relation exists, redirect to home
            django_messages.error(request, "Relation not found.")
            return redirect("home")

    # If the method is not GET, you might want to handle it here (e.g., return an error or a response)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# @login_required(login_url="login")
# @csrf_exempt
# def message_list(request, sender=None, receiver=None):
#     if request.method == "GET":
#         messages = Messages.objects.filter(
#             sender_name=sender, receiver_name=receiver, seen=False
#         )
#         serializer = MessageSerializer(
#             messages, many=True, context={"request": request}
#         )
#         for message in messages:
#             message.seen = True
#             message.save()
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
