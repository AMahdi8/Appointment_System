# Generated by Django 5.1.1 on 2024-09-28 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_remove_medic_age_remove_medic_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/patients/', verbose_name='image'),
        ),
    ]
