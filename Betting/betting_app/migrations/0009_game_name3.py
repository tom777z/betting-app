# Generated by Django 4.2.5 on 2023-10-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0008_game_name2'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='name3',
            field=models.CharField(default='test', max_length=200),
        ),
    ]
