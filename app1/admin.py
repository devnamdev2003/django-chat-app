from django.contrib import admin
from .models import UserRelation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Define a custom admin class for the User model
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )


# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)


class UserRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "friend", "accepted")
    list_filter = ("user", "accepted")
    search_fields = ("user__username", "friend")


admin.site.register(UserRelation, UserRelationAdmin)
