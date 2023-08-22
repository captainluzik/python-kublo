# Generated by Django 4.2.4 on 2023-08-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cabinet_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                max_length=150,
                unique=True,
                verbose_name="username",
            ),
        ),
    ]
