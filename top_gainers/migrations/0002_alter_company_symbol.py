# Generated by Django 4.2.9 on 2024-01-25 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('top_gainers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='symbol',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
