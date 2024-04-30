# Generated by Django 5.0.4 on 2024-04-29 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ricks', '0003_remove_rick_is_morty_alive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Morty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('universe', models.CharField(max_length=255, unique=True)),
                ('is_alive', models.BooleanField(default=True)),
                ('paired_rick', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='ricks.rick')),
            ],
        ),
    ]