# Generated by Django 5.0.1 on 2024-04-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0008_hash"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
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
                ("aadhar_number", models.CharField(max_length=16)),
                ("verification_code", models.CharField(max_length=10)),
            ],
        ),
    ]
