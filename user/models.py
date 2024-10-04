from math import ceil
from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from clinic.models import Clinic


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number is required.')
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'

    phone_number = models.CharField(
        _('phone_number'),
        max_length=20,
        unique=True
    )

    is_medic = models.BooleanField(
        _('medic'),
        default=False
    )

    is_patient = models.BooleanField(
        _('patient'),
        default=False
    )

    first_name = models.CharField(
        _('first_name'),
        max_length=255,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        _('last_name'),
        max_length=255,
        null=True,
        blank=True
    )

    age = models.PositiveSmallIntegerField(
        _('age'),
        null=True,
        blank=True
    )

    username = None

    objects = UserManager()

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        return str(self.phone_number)
    
    def save(self, *args, **kwargs):
        if self.is_medic == True:
            self.is_patient = False

        elif self.is_patient == True:
            self.is_medic = False
            
        return super().save(*args, **kwargs)


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient'
    )

    image = models.ImageField(
        _('image'),
        upload_to='media/patients/',
        blank=True,
        null=True
    )

    address = models.TextField(
        _('address'),
        blank=True,
        null=True
    )

    medical_history = models.TextField(
        _('medical_history'),
        blank=True,
        null=True
    )

    insurance_info = models.CharField(
        _('insurance_info'),
        max_length=100,
        blank=True,
        null=True
    )

    blood_group = models.CharField(
        _('blood_group'),
        max_length=20,
        blank=True,
        null=True
    )

    drug_allergy = models.TextField(
        _('drug_allergy'),
        blank=True,
        null=True
    )

    special_medicine = models.TextField(
        _('special_medicine'),
        blank=True,
        null=True
    )

    systemic_diseases = models.TextField(
        _('systemic_diseases'),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'patient {self.user}'


class Medic(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='medic'
    )

    image = models.ImageField(
        _('image'),
        upload_to='media/medics/',
        null=True,
        blank=True
    )

    specialization = models.CharField(
        _('specialization'),
        max_length=255
    )

    medical_system_number = models.CharField(
        _('medical_number'),
        max_length=20
    )

    accepted = models.BooleanField(_('accepted'), default=False)

    def __str__(self) -> str:
        return f'{self.user} {self.specialization} specialize.'


class TimeSlot(models.Model):
    DAY_OF_WEEK_CHOICES = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday'))
    ]

    medic = models.ForeignKey(
        Medic,
        on_delete=models.CASCADE,
        related_name='available_times'
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='set_appointment'
    )

    day_of_week = models.IntegerField(
        _('day_of_week'),
        choices=DAY_OF_WEEK_CHOICES
    )

    start_time = models.TimeField(_('start_time'))
    end_time = models.TimeField(_('end_time'))

    avg_visit_time = models.PositiveSmallIntegerField(
        _('avg_visit_time'),
    )

    avg_patient_visit = models.PositiveSmallIntegerField(
        _('avg_patient_visit'),
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        _('active'),
        default=True
    )

    def __str__(self):
        return f"{self.medic} - {self.day_of_week} {self.start_time} to {self.end_time} at {self.clinic.address}"

    class Meta:
        unique_together = ('medic', 'day_of_week')
