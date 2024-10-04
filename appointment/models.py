from django.db import models
from django.utils.translation import gettext_lazy as _

from medical_records.models import MedicalRecord
from user.models import Patient, TimeSlot


class Prescription(models.Model):
    prescription_number = models.CharField(
        _('prescription_number')
    )

    drugs = models.TextField(
        _('drugs')
    )


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.DO_NOTHING,
        related_name='appointments'
    )

    time = models.ForeignKey(
        TimeSlot,
        on_delete=models.DO_NOTHING,
        related_name='appointments'
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.DO_NOTHING,
        related_name='appointments',
        blank=True,
        null=True
    )

    prescription = models.OneToOneField(
        Prescription,
        on_delete=models.CASCADE,
        related_name='prescription'
    )

    short_description = models.CharField(
        _('description'),
        max_length=255,
        blank=True
    )

    appointment_datetime = models.DateTimeField(
        _('appointment datetime'),
        blank=True,
        null=True
    )

    appointment_number = models.PositiveSmallIntegerField(
        _('appointment_number'),
    )

    def __str__(self) -> str:
        return f'{self.patient} -> {self.time.medic} at {self.appointment_datetime} in {self.time.clinic}'
