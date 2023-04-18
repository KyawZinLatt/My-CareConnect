# Generated by Django 4.1.5 on 2023-02-05 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("callcenter", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="age_range",
            field=models.CharField(
                choices=[
                    ("BelowFifteen", "BelowFifteen"),
                    ("FifteenAndAbove", "FifteenAndAbove"),
                ],
                max_length=255,
            ),
        ),
    ]
