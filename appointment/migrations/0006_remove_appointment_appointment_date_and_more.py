# Generated by Django 5.1.1 on 2024-09-26 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_alter_appointment_appointment_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='appointment datetime'),
        ),
    ]
