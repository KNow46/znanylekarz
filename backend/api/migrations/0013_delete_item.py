# Generated by Django 5.1.4 on 2024-12-07 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_customuser_doctor_patient_opinion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
    ]