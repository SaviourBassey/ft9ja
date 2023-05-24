from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register_view"),
    path("login/", views.LoginView.as_view(), name="login_view"),
]
