# Generated by Django 4.2.5 on 2023-10-24 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0017_remove_game_collection_delete_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Round 1', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='betting_app.round'),
        ),
    ]
