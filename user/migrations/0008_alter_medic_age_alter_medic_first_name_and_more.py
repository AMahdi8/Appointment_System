# Generated by Django 5.1.1 on 2024-09-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_managers_remove_user_age_medic_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medic',
            name='age',
            field=models.PositiveSmallIntegerField(verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='medic',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='medic',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='last_name'),
        ),
        migrations.AlterField(
            model_name='medic',
            name='medical_system_number',
            field=models.CharField(max_length=20, verbose_name='medical_system'),
        ),
        migrations.AlterField(
            model_name='medic',
            name='specialization',
            field=models.CharField(max_length=255, verbose_name='specialization'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.PositiveSmallIntegerField(verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='blood_group',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='blood_group'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='drug_allergy',
            field=models.TextField(blank=True, null=True, verbose_name='drug_allergy'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='insurance_info',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='insurance_info'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='last_name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='medical_history',
            field=models.TextField(blank=True, null=True, verbose_name='medical_history'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='special_medicine',
            field=models.TextField(blank=True, null=True, verbose_name='special_medicine'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='systemic_diseases',
            field=models.TextField(blank=True, null=True, verbose_name='systemic_diseases'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='clinic_address',
            field=models.TextField(verbose_name='clinic_address'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, 'Saturday'), (2, 'Sunday'), (3, 'Monday'), (4, 'Tuesday'), (5, 'Wednesday'), (6, 'Thursday'), (7, 'Friday')], verbose_name='day_of_week'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(verbose_name='end_time'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.TimeField(verbose_name='start_time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='phone_number'),
        ),
    ]
