# Generated by Django 4.2.5 on 2023-10-24 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0013_remove_game_collection_alter_collection_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='betting_app.collection'),
        ),
    ]