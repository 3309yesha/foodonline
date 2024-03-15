# Generated by Django 5.0.3 on 2024-03-14 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_lettitude_userprofile_letitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_2',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]