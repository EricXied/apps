# Generated by Django 4.1 on 2024-01-04 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0007_savefilefield_alter_post_create_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="create_at",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2024, 1, 3, 22, 33, 58, 108221)
            ),
        ),
    ]
