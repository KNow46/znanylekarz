# Generated by Django 5.1.4 on 2024-12-05 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customuser_doctor_patient'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text="User's groups", related_name='customuser_set', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='User permissions', related_name='customuser_set', to='auth.permission', verbose_name='Permissions'),
        ),
    ]
