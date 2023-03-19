# Generated by Django 4.1.7 on 2023-03-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.CharField(max_length=100)),
                ('adults', models.IntegerField()),
                ('price_per_night', models.IntegerField()),
                ('code', models.TextField()),
                ('breakfast_included', models.BooleanField()),
            ],
        ),
    ]
