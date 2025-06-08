from django.db import models


class User(models.Model):
    vk_id = models.BigIntegerField(unique=True, verbose_name="VK ID")
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} (id={self.vk_id})"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    number = models.PositiveIntegerField(unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Билет #{self.number} для {self.user.full_name}"


class Draw(models.Model):
    title = models.CharField(max_length=255)
    total_winners = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    winners = models.ManyToManyField("Ticket", blank=True, related_name="draws")

    def __str__(self):
        return f"{self.title} — {self.total_winners} призов"
