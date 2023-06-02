from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.Logout, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("setProfile/", views.ProfileChangeView.as_view(), name="setProfile"),
    path("changePassword/", views.PasswordChangeView.as_view(), name="changePassword"),
]
