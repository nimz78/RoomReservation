# Generated by Django 4.1.7 on 2023-03-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='code',
        ),
        migrations.AlterField(
            model_name='room',
            name='breakfast_included',
            field=models.BooleanField(default=True),
        ),
    ]
