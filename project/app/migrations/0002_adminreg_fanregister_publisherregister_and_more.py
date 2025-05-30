# Generated by Django 5.1.6 on 2025-02-18 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.TextField()),
                ('phone', models.IntegerField()),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FanRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.TextField()),
                ('phone', models.IntegerField()),
                ('password', models.TextField()),
                ('location', models.TextField()),
                ('confirm_password', models.TextField()),
                ('favoriteevent', models.TextField()),
                ('favoriteteam', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PublisherRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.TextField()),
                ('organization', models.TextField()),
                ('password', models.TextField()),
                ('location', models.TextField()),
                ('confirm_password', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='fanprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='EventPublisherProfile',
        ),
        migrations.DeleteModel(
            name='FanProfile',
        ),
    ]
