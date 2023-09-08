from django.contrib import admin
from app1 import views
from django.views.generic import RedirectView
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.LoginPage, name="login"),
    path("signup/", views.SignupPage, name="signup"),
    path("logout/", views.LogoutPage, name="logout"),
    path("user/", views.HomePage, name="home"),
    path("edit/", views.EditProfile, name="edit"),
    path("user/<str:username>/", views.userprofile, name="username"),
    path("add_friend/", views.add_friend, name="add_friend"),
    path("accept_request/", views.accept_request, name="accept_request"),
    path("delete_friend/", views.delete_friend, name="delete_friend"),
    path("search/", views.search, name="search"),
    re_path(r"^.*/$", RedirectView.as_view(pattern_name="login", permanent=False)),
    
    
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
