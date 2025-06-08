from django.db import models


class User(models.Model):
    vk_id = models.BigIntegerField(unique=True, verbose_name="VK ID")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self):
        return f"{self.full_name} (id={self.vk_id})"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", verbose_name="Участник")
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер билета")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

    def __str__(self):
        return f"Билет №{self.number} — {self.user.full_name}"


class Draw(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название розыгрыша")
    total_winners = models.PositiveIntegerField(default=1, verbose_name="Количество победителей")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    winners = models.ManyToManyField("Ticket", blank=True, related_name="draws", verbose_name="Победители")

    class Meta:
        verbose_name = "Розыгрыш"
        verbose_name_plural = "Розыгрыши"

    def __str__(self):
        return f"{self.title} — {self.total_winners} призов"
