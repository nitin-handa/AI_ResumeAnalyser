# Generated by Django 3.2.12 on 2024-05-13 06:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartCV_app', '0003_auto_20240513_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedpdf',
            name='name',
        ),
        migrations.AddField(
            model_name='uploadedpdf',
            name='serial_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='logging',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 5, 13, 11, 31, 45, 463361)),
        ),
    ]
