# Generated by Django 5.0.1 on 2024-03-09 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0009_primaryvoterdatabase_face_image_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="primaryvoterdatabase",
            name="face_image",
        ),
        migrations.RemoveField(
            model_name="secondaryvoterdatabase",
            name="face_image",
        ),
    ]
