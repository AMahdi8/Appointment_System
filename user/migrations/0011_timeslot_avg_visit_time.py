# Generated by Django 5.1.1 on 2024-09-23 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_medic_medical_system_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='avg_visit_time',
            field=models.PositiveSmallIntegerField(default=30, verbose_name='avg_visit_time'),
        ),
    ]
