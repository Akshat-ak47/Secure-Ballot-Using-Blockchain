# Generated by Django 5.0.1 on 2024-03-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0011_official_mobile_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="official",
            name="mobile_number",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
