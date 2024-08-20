# Generated by Django 3.2 on 2024-07-26 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartCV_app', '0012_auto_20240518_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='csv_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, upload_to='static/csv_file/')),
            ],
        ),
        migrations.AlterField(
            model_name='logging',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 7, 26, 15, 8, 30, 173136)),
        ),
    ]