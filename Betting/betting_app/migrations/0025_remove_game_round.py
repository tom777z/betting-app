# Generated by Django 4.2.5 on 2023-10-24 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0024_round_game_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='round',
        ),
    ]
