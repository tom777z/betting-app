# Generated by Django 4.2.5 on 2023-10-24 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0012_alter_game_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='collection',
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(default='Kolejka', max_length=200),
        ),
    ]
