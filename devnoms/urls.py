from django.contrib import admin
from chat.views import *
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginPage, name="login"),
    path("signup/", SignupPage, name="signup"),
    path("logout/", LogoutPage, name="logout"),
    path("user/", HomePage, name="home"),
    path("edit/", EditProfile, name="edit"),
    path("user/<str:username>/", userprofile, name="username"),
    path("add_friend/", add_friend, name="add_friend"),
    path("accept_request/", accept_request, name="accept_request"),
    path("delete_friend/", delete_friend, name="delete_friend"),
    path("search/", search, name="search"),
    # re_path(r"^.*/$", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("chat/<str:username>/", chat, name="chat"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
