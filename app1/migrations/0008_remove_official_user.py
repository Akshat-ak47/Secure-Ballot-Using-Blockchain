# Generated by Django 5.0.1 on 2024-03-06 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0007_official_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="official",
            name="user",
        ),
    ]
