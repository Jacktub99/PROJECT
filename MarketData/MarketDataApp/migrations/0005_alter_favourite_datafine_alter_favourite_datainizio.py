# Generated by Django 5.0.4 on 2024-04-11 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketDataApp', '0004_alter_favourite_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='dataFine',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='dataInizio',
            field=models.CharField(max_length=100),
        ),
    ]
