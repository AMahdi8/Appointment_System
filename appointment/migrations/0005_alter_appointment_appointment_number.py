# Generated by Django 5.1.1 on 2024-09-26 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_alter_appointment_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_number',
            field=models.PositiveSmallIntegerField(verbose_name='appointment_number'),
        ),
    ]
