# Generated by Django 5.0.1 on 2024-04-12 07:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0006_vote"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="aadhar_number",
            field=models.CharField(default=None, max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vote",
            name="username",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="vote",
            name="previous_hash",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="vote",
            name="voter_hash",
            field=models.CharField(max_length=64),
        ),
    ]
