# Generated by Django 5.0.2 on 2024-07-21 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
