from django.db import models


class Login(models.Model):
    """Модель для хранения логинов и паролей от почты."""

    login = models.CharField(
        verbose_name="Логин",
        unique=True,
        max_length=255,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=255,
    )

    class Meta:
        verbose_name = "Логин"
        verbose_name_plural = "Логины"

    def __str__(self):
        return self.login


class Message(models.Model):
    """Модель для хранения сообщений."""

    owner = models.ForeignKey(
        Login,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец",
    )
    theme = models.CharField(
        verbose_name="Тема",
        max_length=200,
    )
    send_date = models.DateTimeField(
        verbose_name="Дата отправки",
    )
    receipt_date = models.DateTimeField(
        verbose_name="Дата получения",
    )
    text = models.TextField(verbose_name="Текст сообщения")
    attachments_list = models.TextField(verbose_name="Список вложений")

    class Meta:
        ordering = ("-send_date",)
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "send_date", "theme"], name="unique_message"
            )
        ]

    def __str__(self):
        return self.theme
