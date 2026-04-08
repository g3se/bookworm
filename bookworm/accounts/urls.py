from django.urls import path

from .views import login


urlpatterns = [
    path("login/", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("register/", login.register_view, name="register"),
    path("address/", login.edit_address_view, name="edit_address"),
    path("profile/edit/", login.edit_profile_view, name="edit_profile"),
]
