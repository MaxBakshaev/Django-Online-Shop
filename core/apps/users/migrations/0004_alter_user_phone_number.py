# Generated by Django 5.1.4 on 2025-02-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Номер телефона'),
        ),
    ]
