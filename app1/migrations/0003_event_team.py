# Generated by Django 5.0.1 on 2024-03-16 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0002_event_dummy_field_team_dummy_field"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("event_id", models.AutoField(primary_key=True, serialize=False)),
                ("event_name", models.CharField(max_length=100)),
                ("num_teams", models.IntegerField()),
                ("event_purpose", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("dummy_field", models.CharField(blank=True, max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="team_images/")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to="app1.event",
                    ),
                ),
            ],
        ),
    ]
