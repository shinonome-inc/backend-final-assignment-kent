# Generated by Django 4.1.4 on 2022-12-21 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_friendship_unique_booking"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="friendship",
            name="updated_at",
        ),
    ]
