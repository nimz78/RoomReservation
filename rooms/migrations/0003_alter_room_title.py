# Generated by Django 4.1.7 on 2023-03-18 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_remove_room_code_alter_room_breakfast_included'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]