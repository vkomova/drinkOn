# Generated by Django 2.1.7 on 2019-03-18 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='google_assigned_id',
            new_name='google_place_id',
        ),
    ]
