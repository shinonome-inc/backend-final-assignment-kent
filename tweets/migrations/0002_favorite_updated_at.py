# Generated by Django 4.1.4 on 2023-01-14 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="favorite",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
