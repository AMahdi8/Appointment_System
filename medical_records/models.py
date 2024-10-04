from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import Medic, Patient


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.DO_NOTHING,
        related_name='medical_patient'
    )

    medic = models.ForeignKey(
        Medic,
        on_delete=models.DO_NOTHING,
        related_name='medical_patient'
    )

    illnes_subject = models.CharField(
        _('illnes_subject'),
        max_length=255,
        blank=True,
        null=True
    )

    illness = models.TextField(
        _('illness'),
        blank=True,
        null=True
    )

    hospitalized = models.BooleanField(
        _('hospitalized'),
        default=False
    )

    related_file = models.FileField(
        _('related_file'),
        upload_to='media/medical_records/',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'patient: {self.patient} -> medic: {self.medic}'

    class Meta:
        unique_together = ('patient', 'medic')
