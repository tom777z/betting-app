# Generated by Django 4.2.5 on 2023-10-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betting_app', '0026_delete_round'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
