# Generated by Django 4.2.5 on 2023-10-24 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0016_game_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='collection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
    ]