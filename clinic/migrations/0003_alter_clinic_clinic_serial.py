# Generated by Django 5.1.1 on 2024-09-25 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_clinic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='clinic_serial',
            field=models.CharField(max_length=30, unique=True, verbose_name='clinic_serial'),
        ),
    ]
