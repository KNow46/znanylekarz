# Generated by Django 5.1.4 on 2024-12-08 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_calendar_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='calendar',
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.doctor'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Calendar',
        ),
    ]
