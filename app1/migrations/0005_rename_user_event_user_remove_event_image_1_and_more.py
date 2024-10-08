# Generated by Django 5.0.1 on 2024-03-24 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0004_remove_event_dummy_field_event_user_event_image_1_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="User",
            new_name="user",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_1",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_2",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_3",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_4",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_5",
        ),
        migrations.RemoveField(
            model_name="event",
            name="team_1",
        ),
        migrations.RemoveField(
            model_name="event",
            name="team_2",
        ),
        migrations.RemoveField(
            model_name="event",
            name="team_3",
        ),
        migrations.RemoveField(
            model_name="event",
            name="team_4",
        ),
        migrations.RemoveField(
            model_name="event",
            name="team_5",
        ),
        migrations.AddField(
            model_name="event",
            name="dummy_field",
            field=models.CharField(blank=True, max_length=1, null=True),
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
