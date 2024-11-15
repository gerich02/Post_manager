from django.shortcuts import render
from django.http import JsonResponse
from .models import Login


def index(request):
    """Главная страница."""

    return render(request, "index.html")


def add_login(request):
    """Добавление логина/пароля."""

    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")

        if not login:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Login is required"
                }
            )

        login_instance, created = Login.objects.update_or_create(
            login=login,
            defaults={"password": password},
        )

        return JsonResponse({
            "status": "created" if created else "updated",
            "message": "Login added successfully",
            "login_id": login_instance.id
        })

    return JsonResponse(
        {
            "status": "error",
            "message": "Invalid request method"
        }
    )


def messages_page(request):
    """страница со списком писем."""

    return render(request, "messages.html")
