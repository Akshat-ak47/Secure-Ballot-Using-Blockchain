# Generated by Django 5.0.1 on 2024-04-12 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0007_vote_aadhar_number_vote_username_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hash",
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
                ("voter_hash", models.CharField(max_length=64)),
                ("previous_hash", models.CharField(max_length=64)),
            ],
        ),
    ]
