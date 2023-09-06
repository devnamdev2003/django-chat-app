from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.SignupPage, name="signup"),
    path("", views.LoginPage, name="login"),
    path("user/", views.HomePage, name="home"),
    path("logout/", views.LogoutPage, name="logout"),
    path("edit/", views.EditProfile, name="edit"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
