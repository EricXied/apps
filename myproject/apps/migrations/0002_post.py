# Generated by Django 4.1 on 2023-12-21 01:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=100)),
                ("body", models.CharField(max_length=100000)),
                (
                    "create_at",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
            ],
        ),
    ]
