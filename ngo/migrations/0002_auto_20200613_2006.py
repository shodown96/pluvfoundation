# Generated by Django 3.0.5 on 2020-06-13 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='intro',
        ),
        migrations.RemoveField(
            model_name='post',
            name='intro',
        ),
        migrations.RemoveField(
            model_name='project',
            name='intro',
        ),
    ]
