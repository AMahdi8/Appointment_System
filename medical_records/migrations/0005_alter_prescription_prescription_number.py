# Generated by Django 5.1.1 on 2024-09-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_records', '0004_alter_medicalrecord_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='prescription_number',
            field=models.CharField(verbose_name='prescription_number'),
        ),
    ]
