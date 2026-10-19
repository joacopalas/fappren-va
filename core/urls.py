from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("healthz/", views.healthz, name="healthz"),
    path("accounts/register/", views.register, name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("test/self/", views.take_test, {"mode": "self"}, name="test_self"),
    path(
        "test/administer/",
        views.take_test,
        {"mode": "administered"},
        name="test_administer",
    ),
    path("results/", views.results_list, name="results"),
    path("results/<int:pk>/", views.result_detail, name="result_detail"),
    path("administration/users/", views.user_management, name="user_management"),
    path(
        "administration/users/<int:user_id>/toggle-admin/",
        views.toggle_admin,
        name="toggle_admin",
    ),
    path(
        "administration/export.xlsx",
        views.export_results_xlsx,
        name="export_xlsx",
    ),
]