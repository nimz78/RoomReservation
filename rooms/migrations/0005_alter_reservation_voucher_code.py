# Generated by Django 4.1.7 on 2023-03-23 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='voucher_code',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
