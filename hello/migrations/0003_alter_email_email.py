# Generated by Django 3.2.11 on 2022-01-19 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_email_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]