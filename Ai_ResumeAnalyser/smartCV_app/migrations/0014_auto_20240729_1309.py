# Generated by Django 3.2 on 2024-07-29 07:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartCV_app', '0013_auto_20240726_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='skills_dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='logging',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 7, 29, 13, 9, 2, 266633)),
        ),
    ]
