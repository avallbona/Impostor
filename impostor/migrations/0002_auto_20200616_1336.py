# Generated by Django 3.0.7 on 2020-06-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("impostor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="impostorlog",
            name="token",
            field=models.CharField(
                blank=True, db_index=True, max_length=36, verbose_name="Token"
            ),
        ),
    ]
