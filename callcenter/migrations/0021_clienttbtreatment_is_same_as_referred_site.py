# Generated by Django 4.0.6 on 2023-06-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0020_sitelocation_provider_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienttbtreatment',
            name='is_same_as_referred_site',
            field=models.BooleanField(null=True),
        ),
    ]