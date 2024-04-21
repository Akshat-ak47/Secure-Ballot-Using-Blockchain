# Generated by Django 5.0.1 on 2024-03-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VoterData",
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
                ("unique_hash", models.CharField(max_length=64, unique=True)),
                ("aadhar_number", models.BigIntegerField()),
                ("primary_password", models.CharField(max_length=255)),
                ("secondary_password", models.CharField(max_length=255)),
            ],
        ),
    ]
