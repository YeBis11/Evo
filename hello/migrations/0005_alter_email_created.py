# Generated by Django 3.2.11 on 2022-01-19 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_alter_email_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]