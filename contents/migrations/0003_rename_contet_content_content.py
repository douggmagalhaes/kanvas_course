# Generated by Django 4.2.4 on 2023-08-24 20:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contents", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="content",
            old_name="contet",
            new_name="content",
        ),
    ]
