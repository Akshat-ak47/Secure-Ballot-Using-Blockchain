# Generated by Django 5.0.1 on 2024-03-16 09:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GovernmentData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("aadhar_number", models.BigIntegerField(unique=True)),
                ("mobile_number", models.BigIntegerField(unique=True)),
                ("age", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Official",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("FULLName", models.CharField(max_length=100)),
                ("Username", models.CharField(max_length=50, unique=True)),
                ("Email", models.EmailField(max_length=254, unique=True)),
                ("Aadhar_Number", models.CharField(max_length=12, unique=True)),
                ("Password", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="YourModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="PrimaryVoterDatabase",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unique_address", models.CharField(max_length=255)),
                ("aadhar_number", models.CharField(max_length=12, unique=True)),
                ("mobile_number", models.CharField(max_length=10)),
                ("primary_pass", models.CharField(max_length=128)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SecondaryVoterDatabase",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unique_address", models.CharField(max_length=255)),
                ("aadhar_number", models.CharField(max_length=12, unique=True)),
                ("mobile_number", models.CharField(max_length=10)),
                ("secondary_pass", models.CharField(max_length=128)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
