# Generated by Django 5.1.1 on 2024-09-16 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medic',
            name='medical_system_number',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
