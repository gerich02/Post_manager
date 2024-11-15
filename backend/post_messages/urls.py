from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "add-login/", views.add_login, name="add-login"
    ),
    path("messages/", views.messages_page, name="messages-page"),
]
