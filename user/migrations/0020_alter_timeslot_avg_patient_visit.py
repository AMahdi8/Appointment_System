# Generated by Django 5.1.1 on 2024-09-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='avg_patient_visit',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='avg_patient_visit'),
        ),
    ]
