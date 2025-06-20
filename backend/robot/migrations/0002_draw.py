# Generated by Django 5.2.2 on 2025-06-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robot", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Draw",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("total_winners", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "winners",
                    models.ManyToManyField(
                        blank=True, related_name="draws", to="robot.ticket"
                    ),
                ),
            ],
        ),
    ]
