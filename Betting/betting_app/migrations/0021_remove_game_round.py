# Generated by Django 4.2.5 on 2023-10-24 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0020_alter_game_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='round',
        ),
    ]
