# Generated by Django 5.0.3 on 2024-03-21 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='vendors',
        ),
    ]
