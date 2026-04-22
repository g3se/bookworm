from django.urls import path

from .views import login, profile


urlpatterns = [
    path("login/", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("register/", login.register_view, name="register"),
    path("address/", profile.edit_address_view, name="edit_address"),
    path("profile/edit/", profile.edit_profile_view, name="edit_profile"),
    path("profile/change-password/", profile.change_password_view, name="change_password"),
]
