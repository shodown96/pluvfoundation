# Generated by Django 3.1.4 on 2020-12-14 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('statement', models.TextField()),
                ('middle_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('address', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=10)),
                ('date_applied', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ['-date_applied'],
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('completed', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('sex', models.CharField(max_length=10)),
                ('about', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('dp', models.ImageField(blank=True, null=True, upload_to='display_pics/')),
                ('location', models.CharField(max_length=100)),
                ('position', models.CharField(blank=True, default='Member', max_length=100, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('subscribed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
    ]