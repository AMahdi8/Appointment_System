# Generated by Django 5.1.1 on 2024-09-26 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_appointment_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='short_description',
            field=models.CharField(blank=True, max_length=255, verbose_name='description'),
        ),
    ]
