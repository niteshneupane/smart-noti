# Generated by Django 4.2.23 on 2025-07-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_deliverystatus_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationpreference',
            old_name='login',
            new_name='unauthorized_login',
        ),
    ]
